"""
account_info.py
~~~~~~~~~~~~~~~
Fetches account balance, positions, and open orders from Binance Testnet.
Then uses LLM to generate a clean natural language summary.
"""

from __future__ import annotations
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

from dotenv import load_dotenv
load_dotenv()

from bot.client import BinanceClient
from bot.logging_config import setup_logger

_log = setup_logger("trading_bot.account_info")

SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a trading assistant. You MUST immediately summarize the account data provided.
Never say 'please hold on' or 'let me check' — the data is already given to you.
Always respond with the actual data. in this format:

**Wallet Balance:** X USDT
**Available Balance:** X USDT

**Open Positions:**
- Symbol:
- Side:
- Size:
- Unrealized PnL: (or 'None' if empty)

**Open Orders:**
- Order ID:
- Symbol:
- Type:
- Side:
- Price:
- Quantity: (or 'None' if empty)

Rules:
- If user asks for balance only → show only balance fields
- If user asks for a specific order ID → show only that order
- If user asks for positions only → show only positions
- If user asks for open orders only → show only open orders
- If user asks for everything → show full format above
Closed orders are not available. If asked, say so once and move on."""),
    ("human", "Account Data: {account_data}\nUser Question: {user_question}")
])

def get_account_summary(client: BinanceClient, user_question: str) -> str:
    try:
        account = client.get_account_info()

        print(json.dumps(account, indent=2))
        # Extract relevant fields
        wallet_balance = next(
            (a.get("walletBalance") for a in account.get("assets", []) if a.get("asset") == "USDT"),
            "N/A"
        )
        available_balance = next(
            (a.get("availableBalance") for a in account.get("assets", []) if a.get("asset") == "USDT"),
            "N/A"
        )
        positions = [
            {
                "symbol": p["symbol"],
                "side": p["positionSide"],
                "size": p["positionAmt"],
                "unrealizedPnL": p["unrealizedProfit"],
                "entryPrice": p["entryPrice"],
            }
            for p in account.get("positions", [])
            if float(p.get("positionAmt", 0)) != 0
        ]

        open_orders = [
            {
                "orderId": o["orderId"],
                "symbol": o["symbol"],
                "type": o["type"],
                "side": o["side"],
                "price": o["price"],
                "quantity": o["origQty"],
                "status": o["status"],
            }
            for o in client.get("/fapi/v1/openOrders", signed=True)
        ]

        summary_data = {
            "wallet_balance_usdt": wallet_balance,
            "available_balance_usdt": available_balance,
            "open_positions": positions,
            "open_orders": open_orders,
        }

        llm = ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL_NAME"),
            temperature=0.3,
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        chain = SUMMARY_PROMPT | llm
        result = chain.invoke({
            "account_data": str(summary_data),
            "user_question": user_question
        })
        return result.content.strip()

    except Exception as e:
        _log.error("Account info fetch failed: %s", e)
        return f"❌ Could not fetch account info: {e}"
