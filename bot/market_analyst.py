"""
market_analyst.py
~~~~~~~~~~~~~~~~~
Fetches live price data from Binance + news from SerperDev,
then uses LLM to generate market analysis and trading suggestions.
"""

from __future__ import annotations
import os
import requests
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

from bot.logging_config import setup_logger

_log = setup_logger("trading_bot.market_analyst")

ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert crypto trading analyst.
Based on the market data, news, and account info provided, give:
1. Current market snapshot (price, 24h change, volume)
2. Brief trend analysis (bullish/bearish/neutral and why)
3. Impact on current holdings (if account info available)
4. Clear trading suggestion with reasoning
5. Risk warning

Important rules:
- Always refer to the specific coin being asked about
- If it's a follow-up question like 'what about SOL' or 'how will this affect me',
  answer in context of the previous conversation
- Be concise and always remind this is not financial advice"""),
    ("human", """Symbol: {symbol}
Market Data:
{market_data}
News: {news}
Account: {account_context}
Question: {question}
Note: If account context is unavailable, skip that section entirely.""")
])


def _fetch_binance_ticker(symbol: str) -> dict:
    try:
        url = "https://testnet.binancefuture.com/fapi/v1/ticker/24hr"
        response = requests.get(url, params={"symbol": symbol}, timeout=10)
        return response.json()
    except Exception as e:
        _log.error("Binance ticker fetch failed: %s", e)
        return {}


def _fetch_binance_klines(symbol: str) -> list:
    try:
        url = "https://testnet.binancefuture.com/fapi/v1/klines"
        response = requests.get(url, params={
            "symbol": symbol,
            "interval": "1h",
            "limit": 24
        }, timeout=10)
        return response.json()
    except Exception as e:
        _log.error("Klines fetch failed: %s", e)
        return []


def _fetch_serper_news(symbol: str) -> str:
    api_key = os.environ.get("SERPER_API_KEY", "")
    if not api_key:
        return "No news available (SERPER_API_KEY not set)."
    try:
        coin = symbol.replace("USDT", "").replace("BUSD", "")
        response = requests.post(
            "https://google.serper.dev/news",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": f"{coin} crypto market news", "num": 5},
            timeout=10,
        )
        data = response.json()
        news_items = data.get("news", [])
        if not news_items:
            return "No recent news found."
        return "\n".join([
            f"- {item.get('title', '')} ({item.get('date', '')})"
            for item in news_items[:5]
        ])
    except Exception as e:
        _log.error("SerperDev fetch failed: %s", e)
        return "Could not fetch news."


import concurrent.futures

def get_market_analysis(symbol: str, user_question: str, account_context: str = "") -> str:
    symbol = symbol.upper()
    if "USDT" not in symbol:
        symbol += "USDT"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        ticker_future  = executor.submit(_fetch_binance_ticker, symbol)
        klines_future  = executor.submit(_fetch_binance_klines, symbol)
        news_future    = executor.submit(_fetch_serper_news, symbol)

        ticker = ticker_future.result()
        klines = klines_future.result()
        news   = news_future.result()

    recent_closes = [k[4] for k in klines[-6:]] if klines else []

    market_data_str = f"""- Last Price: {ticker.get('lastPrice')}
- 24h Change: {ticker.get('priceChangePercent')}%
- 24h High: {ticker.get('highPrice')}
- 24h Low: {ticker.get('lowPrice')}
- Volume: {ticker.get('volume')}
- Recent Closes (last 6h): {recent_closes}"""

    llm = ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL_NAME"),
        temperature=0.4,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    chain = ANALYSIS_PROMPT | llm
    result = chain.invoke({
        "symbol": symbol,
        "market_data": market_data_str,
        "news": news,
        "question": user_question,
        "account_context": account_context,
    })
    return result.content.strip()