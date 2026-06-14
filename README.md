<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=800&size=42&pause=1000&color=F0B90B&center=true&vCenter=true&width=600&lines=FuturesAI;Talk+to+the+Market.;Trade+with+Intelligence." alt="FuturesAI" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-F0B90B?style=for-the-badge&logo=python&logoColor=black)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-02C076?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Binance](https://img.shields.io/badge/Binance-Futures_Testnet-F0B90B?style=for-the-badge&logo=binance&logoColor=black)](https://testnet.binancefuture.com)

<br/>

> **An AI-powered conversational trading assistant.**
> Type what you want. The AI does the rest.

<br/>

[What Is This?](#-what-is-this) • [Features](#-features) • [How It Works](#-how-it-works) • [Tech Stack](#-tech-stack) • [Setup](#-getting-started) • [Usage](#-how-to-use-it) • [FAQ](#-faq)

---

</div>

## 💡 What Is This?

Most trading platforms expect you to already know what you're doing — learn the interface, understand order types, read charts, manage dashboards.

**FuturesAI flips that completely.**

You just type, in plain English, and the AI figures out the rest.

```
You  →  "Should I buy ETH right now?"

AI   →  Fetches live ETH price from Binance
     →  Pulls latest ETH news from the web
     →  Checks your current holdings and open positions
     →  Generates a data-driven analysis with a clear suggestion
     →  "ETH is showing a slight bullish trend (+0.9% in 24h).
         Given your current short position, consider waiting
         for a pullback before entering a long..."
```

```
You  →  "Buy 0.1 ETH at market price"

AI   →  Understands the intent
     →  Validates the order parameters
     →  Shows you a summary: ETHUSDT | BUY | MARKET | 0.1
     →  Waits for your confirmation
     →  Places the order on Binance Futures Testnet
     →  "✅ Order placed! ID: 9730044657 | Status: NEW"
```

> 🧪 **100% Safe** — Built on Binance Futures Testnet. Simulated environment. No real money. Ever.

---

## ✨ Features

### 🗣️ Natural Language Trading
Forget memorizing commands or clicking through menus. Talk to the bot like you'd talk to a trading assistant.

| You say | Bot does |
|---|---|
| *"Buy 0.01 BTC at market price"* | Places a MARKET BUY order |
| *"Sell 0.5 ETH if it hits 2000"* | Places a LIMIT SELL order at $2000 |
| *"What's my balance?"* | Fetches and summarizes your account |
| *"Should I buy SOL right now?"* | Analyzes market + news + your holdings |
| *"What about ETH?"* | Remembers context, analyzes ETH next |

---

### 📈 Place Orders — Market & Limit
- **MARKET orders** — execute instantly at the best available price
- **LIMIT orders** — set your target price, order waits until market reaches it
- **Confirmation flow** — every order shows a summary before placing. You always have the chance to cancel.
- **Smart validation** — catches errors before they reach the API (wrong side, missing price, invalid symbol)

---

### 💼 Portfolio Management
Ask about your account in plain English:

```
"What's my balance?"
"Show my open positions"
"Do I have any open orders?"
"Tell me about order 15145608719"
```

The bot fetches live data from your Binance testnet account and presents it cleanly — wallet balance, available margin, open positions with unrealized PnL, and all active orders.

---

### 🔍 AI Market Intelligence
This is where it gets powerful. Ask any market question and the bot:

1. Fetches **live price data** from Binance (last price, 24h change, high/low, volume, recent candles)
2. Pulls **real-time news** via SerperDev web search
3. Checks your **current holdings** so suggestions are personalized
4. Sends everything to **GPT-4o-mini** which generates a structured analysis

```
1. Market Snapshot     ← live Binance data
2. Trend Analysis      ← bullish / bearish / neutral + reasoning
3. Impact on Holdings  ← how it affects YOUR positions specifically
4. Trading Suggestion  ← clear recommendation with reasoning
5. Risk Warning        ← always honest about uncertainty
```

---

### 🧠 Conversational Memory
The bot remembers what you've discussed within a session. Follow-up questions work naturally:

```
You:  "Analyze BTC"
Bot:  [BTC analysis]

You:  "What about ETH?"           ← bot knows you want ETH analysis
Bot:  [ETH analysis]

You:  "How will this affect me?"  ← bot ties market data to your holdings
Bot:  [Personalized impact assessment]
```

---

## 🏗️ How It Works

FuturesAI uses a **multi-agent AI architecture** where each component has exactly one responsibility.

```
┌─────────────────────────────────────────────────────┐
│                    You Type                          │
│         "Should I buy ETH right now?"               │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Intent Classifier                       │
│              (LangChain + GPT)                       │
│                                                      │
│  PLACE_ORDER? CHECK_HOLDINGS? MARKET_ANALYSIS?       │
│  → Decides: MARKET_ANALYSIS                         │
└──────┬──────────────┬─────────────────┬─────────────┘
       │              │                 │
       ▼              ▼                 ▼
  ┌─────────┐  ┌───────────┐  ┌─────────────────┐
  │ LLM     │  │ Account   │  │ Market Analyst  │
  │ Parser  │  │ Info      │  │                 │
  │         │  │           │  │ Binance prices  │
  │ Extracts│  │ Fetches   │  │ + SerperDev     │
  │ order   │  │ balance,  │  │ news + GPT      │
  │ params  │  │ positions │  │ analysis        │
  └────┬────┘  └─────┬─────┘  └────────┬────────┘
       │              │                 │
       └──────────────▼─────────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │    Validators                │
       │    (check everything first)  │
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │    Binance Client            │
       │    HMAC-SHA256 signing       │
       │    REST API calls            │
       └──────────────┬───────────────┘
                      │
                      ▼
       ┌──────────────────────────────┐
       │    Streamlit Chat UI         │
       │    Clean response to you     │
       └──────────────────────────────┘
```

### Why This Matters

Each layer is **completely independent**:
- The AI never directly touches the Binance API
- The API layer never touches the AI
- Validation always runs before any network call
- Errors are caught at the right layer and explained in plain English

This is what **production-grade AI architecture** looks like.

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **UI** | Streamlit | Fast, clean chat interface — no frontend code needed |
| **LLM Orchestration** | LangChain + LangChain-OpenAI | Manages prompts, memory, and model calls cleanly |
| **Language Model** | GPT-4o-mini | Fast, affordable, highly capable for structured tasks |
| **Market Data** | Binance Futures Testnet REST API | Real-time prices, candles, account data |
| **News & Search** | SerperDev API | Live web search for crypto news |
| **API Security** | HMAC-SHA256 | Every request cryptographically signed |
| **Logging** | Python logging | Structured file + console logs for every action |
| **Config** | python-dotenv | Clean environment variable management |

---

## 📁 Project Structure

```
FuturesAI/
│
├── app.py                      ← Streamlit chat UI — main entry point
├── styles.py                   ← All CSS (dark theme, animations, fonts)
├── requirements.txt
├── .env.example
│
├── bot/
│   ├── client.py               ← Binance REST client (signing, HTTP, error handling)
│   ├── orders.py               ← Order placement (MARKET, LIMIT, STOP_MARKET)
│   ├── validators.py           ← Input validation before any API call
│   ├── llm_parser.py           ← GPT extracts order params from natural language
│   ├── intent_classifier.py    ← GPT classifies what the user wants
│   ├── market_analyst.py       ← Live data + news + GPT analysis
│   ├── account_info.py         ← Fetches and summarizes account data
│   ├── error_messages.py       ← User-friendly error messages (no API codes)
│   └── logging_config.py       ← Structured logging setup
│
└── logs/
    ├── market_order_sample.log
    └── limit_order_sample.log
```

---

## 🚀 Getting Started

### What You'll Need

Before starting, make sure you have:

- ✅ **Python 3.11+** installed
- ✅ A free **Binance Futures Testnet** account
- ✅ An **OpenAI API key**
- ✅ A **SerperDev API key** (free tier works)

---

### Step 1 — Get Your Binance Testnet Keys

> This is the most important step. Use testnet keys ONLY — not your real Binance keys.

1. Go to **[testnet.binancefuture.com](https://testnet.binancefuture.com)**
2. Sign in with your **GitHub account** (no registration needed)
3. Click **API Management → Generate**
4. Copy both the **API Key** and **Secret Key** immediately *(secret shown only once)*

---

### Step 2 — Clone & Install

```bash
git clone https://github.com/yourusername/ai-trading-assistant.git
cd ai-trading-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate       # macOS / Linux
# OR
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### Step 3 — Configure Your Keys

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
SERPER_API_KEY=your_serperdev_api_key_here
```

---

### Step 4 — Run

```bash
streamlit run app.py
```

Your browser opens automatically at `http://localhost:8501` 🎉

---

## 💬 How to Use It

### Placing Orders

```
"Buy 0.01 BTC at market price"
"Sell 0.5 ETH at limit price of 2000"
"Buy 100 SOL at market"
"Sell 0.3 BTC if it hits 70000"
```

> ⚠️ **Every order shows a confirmation screen before placing.** You always review before anything executes.

---

### Checking Your Account

```
"What's my balance?"
"Show my open positions"
"Do I have any open orders?"
"What is order 15145608719?"
"How much margin do I have available?"
```

---

### Market Analysis

```
"Should I buy ETH right now?"
"What's the current BTC trend?"
"Analyze SOL for me"
"Is DOGE bullish or bearish?"
"How will the market affect my holdings?"
```

---

### Follow-Up Questions

```
"Analyze BTC"           → full BTC analysis
"What about ETH?"       → ETH analysis (bot remembers context)
"Should I buy it?"      → ETH suggestion (bot knows what "it" means)
"How does this affect me?" → personalized impact on your holdings
```

---

## ⚠️ Known Limitations

| Limitation | Explanation |
|---|---|
| **Testnet only** | Hardcoded to Binance Futures Testnet — no real money |
| **Minimum order $5** | Binance requires minimum order value of $5 USD |
| **MARKET order status** | May show `NEW` on testnet due to no real traders — normal |
| **STOP_MARKET** | Implemented in code but testnet endpoint doesn't support it |
| **Closed orders** | Historical order data not available via standard endpoint |
| **Session memory** | Conversation resets on page refresh — no persistent storage |

---

## 🙋 FAQ

**Will this use my real money?**
No. The bot is hardcoded to Binance Futures Testnet — a completely separate simulation environment. Real Binance keys won't even work here.

**Do I need trading experience?**
No. That's the whole point. Type what you want in plain English.

**Why does my market order show "Status: NEW"?**
The testnet has no real traders, so market orders sometimes don't fill immediately. This doesn't happen on the live exchange.

**Why is there a $5 minimum order?**
That's Binance's rule, not ours. For very cheap coins (e.g. ROSE at $0.006), you'd need 800+ units to hit the $5 minimum.

**Can I use my own API keys?**
Yes — add your testnet keys to `.env`. Never use real Binance keys with this project.

**Is this financial advice?**
No. All AI analysis is for educational and demonstration purposes only.

---

## 📋 Assumptions

1. Testnet only — base URL hardcoded to `https://testnet.binancefuture.com`
2. Hedge mode OFF — all orders use `positionSide=BOTH` (default on new accounts)
3. LIMIT orders default to GTC (Good Till Cancelled)
4. Designed as a single-user portfolio demo, not a multi-user production system
5. All AI analysis is for demonstration purposes — not financial advice

---

<div align="center">

---

Built with ⚡ by **Avisha** — AI Engineer

*Portfolio project — for educational purposes only. Not financial advice.*

</div>
