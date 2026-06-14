from __future__ import annotations
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os

INTENTS = ["PLACE_ORDER", "CHECK_HOLDINGS", "MARKET_ANALYSIS", "GENERAL"]

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Classify the user message into exactly one of these intents:

    PLACE_ORDER     — buy, sell, place, order, trade
    CHECK_HOLDINGS  — balance, positions, open orders, order ID, 
                    holdings, account, portfolio, "tell me about order",
                    "open positions", "my orders", "what are my", "show me my"
    MARKET_ANALYSIS — trend, analysis, should I buy, price, market, what about X coin
    GENERAL         — greetings, what can you do, explanations, anything else

    Critical rules:
    - Any message containing an Order ID → always CHECK_HOLDINGS
    - Any message with "position", "order", "balance", "holdings" → always CHECK_HOLDINGS
    - Single word like "btc" after account questions → CHECK_HOLDINGS
    - When in doubt → CHECK_HOLDINGS over GENERAL
    - Return only the intent word. Nothing else."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{message}")
])


def classify_intent(message: str, history: list = []) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.environ.get("OPENAI_API_KEY"))
    chain = PROMPT | llm
    result = chain.invoke({
        "message": message,
        "history": history[-6:]  
    })
    intent = result.content.strip().upper()
    return intent if intent in INTENTS else "GENERAL"