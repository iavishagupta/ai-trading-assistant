"""
app.py
~~~~~~
Streamlit chat interface for the AI Trading Assistant.
"""

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from dotenv import load_dotenv
load_dotenv()

from bot.client import BinanceClient, BinanceAPIError, BinanceNetworkError
from bot.llm_parser import parse_order, extract_symbol
from bot.orders import place_order
from bot.validators import validate_all, ValidationError
from bot.intent_classifier import classify_intent
from bot.account_info import get_account_summary
from bot.market_analyst import get_market_analysis

from styles import STYLES

# ── Page config ────────────────────────────────────────────────────────────────
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="F-AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state=st.session_state.sidebar_state
)

st.title("FuturesAI")
st.caption("Portfolio project leveraging Binance Futures Testnet for AI-assisted trading.")

with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input("Binance Testnet API Key", type="password")
    api_secret = st.text_input("Binance Testnet API Secret", type="password")
    
    if api_key and api_secret:
        st.session_state.binance_api_key = api_key
        st.session_state.binance_api_secret = api_secret
        st.success("✅ Connected")
        
        # 3. Change state to collapsed and force a rerun if it isn't already closed
        if st.session_state.sidebar_state != "collapsed":
            st.session_state.sidebar_state = "collapsed"
            st.rerun() # Forces the page config to load with the 'collapsed' layout
            
    else:
        # Keep sidebar open if credentials are missing
        st.session_state.sidebar_state = "expanded"
        st.warning("Enter your Binance Testnet keys to start")
        st.text("Note: API keys are not saved and will be deleted upon session termination.")
        st.stop()


# ──  UI ────────────────────────────────────────────────────────────────────────
st.markdown(STYLES, unsafe_allow_html=True)

st.markdown("""
<div class="bg-symbols" aria-hidden="true">
  <span>₿</span><span>⟨/⟩</span><span>∑</span><span>Ξ</span>
  <span>◈</span><span>⌬</span><span>₿</span><span>⟨/⟩</span>
  <span>∇</span><span>⬡</span><span>⟁</span><span>◈</span>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": (
            "Hi! I can help you with:\n"
            "- 📈 **Place orders** — *'Buy 0.01 BTC at market price'*\n"
            "- 💼 **Check holdings** — *'What's my balance?'*\n"
            "- 🔍 **Market analysis** — *'Should I buy ETH right now?'*"
        )}
    ]
if "pending_order" not in st.session_state:
    st.session_state.pending_order = None

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_client() -> BinanceClient:
    return BinanceClient(
        api_key=st.session_state.binance_api_key,
        api_secret=st.session_state.binance_api_secret
    )

def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})

def format_order_summary(params: dict) -> str:
    lines = [
        "Here's what I'll place:",
        f"- **Symbol:** {params['symbol']}",
        f"- **Side:** {params['side']}",
        f"- **Type:** {params['order_type']}",
        f"- **Quantity:** {params['quantity']}",
    ]
    if params.get("price"):
        lines.append(f"- **Price:** {params['price']}")
    lines.append("\nConfirm?")
    return "\n".join(lines)


# ── Render chat history ────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Confirmation buttons — rendered AFTER chat history ─────────────────────────
if st.session_state.pending_order:
    with st.chat_message("assistant"):
        st.markdown("Confirm this order?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm", use_container_width=True, key="confirm_btn"):
                params = st.session_state.pending_order
                st.session_state.pending_order = None
                try:
                    client = get_client()
                    result = place_order(client, validated_params=params)
                    msg = (
                        f"✅ **Order placed!**\n"
                        f"- Order ID: `{result['orderId']}`\n"
                        f"- Status: **{result['status']}**\n"
                        f"- Executed Qty: {result['executedQty']}\n"
                        + (f"- Avg Price: {result['avgPrice']}" if float(result.get("avgPrice") or 0) > 0 else "")
                    )
                except BinanceAPIError as e:
                    msg = f"❌ {e.friendly}"
                except BinanceNetworkError as e:
                    msg = f"❌ Network error: {e}"
                except Exception as e:
                    msg = f"❌ Unexpected error: {e}"
                add_message("assistant", msg)
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True, key="cancel_btn"):
                st.session_state.pending_order = None
                add_message("assistant", "Order cancelled. What else can I help you with?")
                st.rerun()

# ── Chat input ─────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Ask me anything about trading..."):
    add_message("user", user_input)

    # Handle cancel explicitly before anything else
    if user_input.strip().lower() in ["cancel", "no", "cancel order", "don't place", "stop"]:
        if st.session_state.pending_order:
            st.session_state.pending_order = None
            add_message("assistant", "Order cancelled. What else can I help you with?")
        else:
            add_message("assistant", "Nothing to cancel. How can I help you?")
        st.rerun()
        st.stop()

    # Build history
    history = []
    for msg in st.session_state.messages[:-1]:
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            history.append(AIMessage(content=msg["content"]))

    with st.spinner("Thinking..."):
        intent = classify_intent(user_input, history=history)

        if intent == "PLACE_ORDER":
            parsed = parse_order(user_input, history=history)
            if "error" in parsed:
                response = f"❌ {parsed['error']}"
                add_message("assistant", response)
            else:
                try:
                    validated = validate_all(
                        symbol=parsed.get("symbol", "BTCUSDT"),
                        side=parsed.get("side", ""),
                        order_type=parsed.get("order_type", "MARKET"),
                        quantity=parsed.get("quantity", 0),
                        price=parsed.get("price"),
                    )
                    st.session_state.pending_order = validated
                    add_message("assistant", format_order_summary(validated))
                except ValidationError as e:
                    add_message("assistant", f"❌ Validation error: {e}")

        elif intent == "CHECK_HOLDINGS":
            try:
                client = get_client()
                response = get_account_summary(client, user_input)
            except Exception as e:
                response = f"❌ Could not fetch account info: {e}"
            add_message("assistant", response)

        elif intent == "MARKET_ANALYSIS":
            context = user_input
            for msg in history[-4:]:
                if hasattr(msg, 'content'):
                    context += " " + msg.content
            symbol = extract_symbol(context, history)
            try:
                client = get_client()
                account_context = get_account_summary(client, user_input)
            except Exception as e:
                account_context = f"Account info unavailable: {str(e)}"
                print(f"DEBUG account error: {e}")  # shows in terminal
            response = get_market_analysis(symbol, user_input, account_context=account_context)
            add_message("assistant", response)

        else:
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.4,
                api_key=os.environ.get("OPENAI_API_KEY")
            )
            result = llm.invoke(
                f"""You are a focused AI trading assistant for Binance Futures Testnet.
You ONLY support MARKET and LIMIT orders.
You can also check holdings, balance, open orders, and analyze market trends.
Do NOT mention Stop-Limit, Take Profit, OCO or any unsupported order types.
Keep responses concise and professional.
User message: {user_input}"""
            )
            add_message("assistant", result.content.strip())

    st.rerun()
