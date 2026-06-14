from __future__ import annotations
import json, os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv
load_dotenv()

from bot.logging_config import setup_logger

_log = setup_logger("trading_bot.llm_parser")

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a trading order parser. Extract order details ONLY from the current message.
Return ONLY a valid JSON object with these exact keys:
symbol — trading pair uppercase with USDT suffix e.g. ROSEUSDT, SOLUSDT, BTCUSDT. Required.
side — must be exactly BUY or SELL. Required.
order_type — must be exactly MARKET or LIMIT. If price is mentioned use LIMIT, otherwise MARKET.
quantity — any positive number including decimals like 0.01, 5, 1000. Required.
price — number if LIMIT order, null if MARKET.

Rules:
- ANY positive number is a valid quantity — never reject based on size
- ANY coin name is valid — always append USDT suffix
- Only return {{"error": "missing side or quantity"}} if side OR quantity is truly absent
- Return JSON only. No markdown. No explanation."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{message}")
])

def parse_order(user_message: str, history: list = []) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.environ.get("OPENAI_API_KEY"))
    chain = PROMPT | llm
    result = chain.invoke({"message": user_message, "history": history})
    raw = result.content.strip()
    _log.debug("OpenAI response: %s", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Could not parse order from your message. Please try again."}

from langchain_openai import ChatOpenAI

def extract_symbol(message: str, history: list = []) -> str:
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"), temperature=0, api_key=os.environ.get("OPENAI_API_KEY"))
    
    history_text = ""
    for msg in history[-4:]:
        if hasattr(msg, 'content'):
            role = "User" if msg.type == "human" else "Assistant"
            history_text += f"{role}: {msg.content}\n"

    prompt = f"""Extract the crypto symbol from the CURRENT MESSAGE first.
Only use conversation history if current message has no coin mentioned.
Return uppercase symbol with USDT suffix e.g. SOLUSDT, ETHUSDT, BTCUSDT.
If truly nothing found anywhere, return BTCUSDT.

Conversation history (use only as fallback):
{history_text}

Current message (highest priority): {message}

Return only the symbol. Nothing else."""
    result = llm.invoke(prompt)
    return result.content.strip().upper()