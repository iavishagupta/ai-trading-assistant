# Binance Futures Testnet — Trading Bot

A clean, structured Python CLI application that places orders on the **Binance Futures Testnet (USDT-M)**.

Built for the Python Developer application task.

---

## Features

| Feature | Detail |
|---|---|
| Order types | MARKET, LIMIT, STOP\_MARKET (bonus) |
| Sides | BUY and SELL |
| CLI | `argparse`-powered with `--dry-run` and `--json` flags |
| Logging | Structured file + console logging (DEBUG to file, INFO to console) |
| Validation | Full input validation with clear error messages |
| Error handling | API errors, network failures, and invalid input all handled gracefully |
| Credentials | Via `.env` file or environment variables |

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package marker
│   ├── client.py            # Binance REST client (signing, HTTP, error handling)
│   ├── orders.py            # Order placement logic (MARKET / LIMIT / STOP_MARKET)
│   ├── validators.py        # Input validation layer
│   └── logging_config.py   # Shared logger setup (file + console)
├── logs/                    # Auto-created on first run
│   ├── market_order_sample.log
│   └── limit_order_sample.log
├── cli.py                   # CLI entry point
├── .env.example             # Template for API credentials
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone / download the project

```bash
git clone https://github.com/YOUR_USERNAME/trading_bot.git
cd trading_bot
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate it:
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Binance Futures Testnet API credentials

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Sign in with your GitHub account (no registration needed)
3. Navigate to **API Management** → **Generate**
4. Copy your **API Key** and **Secret Key**

### 5. Set up your credentials

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```
BINANCE_API_KEY=your_actual_api_key
BINANCE_API_SECRET=your_actual_api_secret
```

> **Alternatively**, pass credentials directly via flags (see examples below).

---

## How to Run

### Basic syntax

```bash
python cli.py --symbol SYMBOL --side SIDE --type ORDER_TYPE --quantity QTY [--price PRICE] [--stop-price STOP]
```

### Examples

#### Market BUY order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

#### Market SELL order
```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.1
```

#### Limit BUY order (buy if price drops to $62,000)
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 62000
```

#### Limit SELL order (sell if price rises to $72,000)
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 72000
```

#### Stop-Market order — bonus type (trigger market sell if price falls to $60,000)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.01 --stop-price 60000
```

#### Dry run (validate without placing the order)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 --dry-run
```

#### Get raw JSON response
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 --json
```

#### Pass API keys directly (no .env needed)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 \
  --api-key YOUR_KEY --api-secret YOUR_SECRET
```

---

## Sample Output

```
╔══════════════════════════════════════════════╗
║   Binance Futures Testnet — Trading Bot      ║
╚══════════════════════════════════════════════╝

── Order Request ──────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01

── Order Response ─────────────────────────────
  Order ID      : 4254133
  Status        : FILLED
  Executed Qty  : 0.010
  Avg Price     : 67423.50000

✔  Order placed successfully!
```

---

## Logging

Logs are automatically written to the `logs/` directory as:
```
logs/trading_bot_YYYY-MM-DD.log
```

- **File** receives DEBUG-level logs (full request/response detail)
- **Console** receives INFO-level logs (clean summaries)

Sample log files from actual testnet orders are included in `logs/`.

---

## All CLI Flags

| Flag | Required | Description |
|---|---|---|
| `--symbol` | ✅ | Trading pair (e.g. `BTCUSDT`) |
| `--side` | ✅ | `BUY` or `SELL` |
| `--type` | ✅ | `MARKET`, `LIMIT`, or `STOP_MARKET` |
| `--quantity` | ✅ | Amount of base asset to trade |
| `--price` | For LIMIT | Limit price |
| `--stop-price` | For STOP\_MARKET | Stop trigger price |
| `--api-key` | Optional | Overrides `BINANCE_API_KEY` env var |
| `--api-secret` | Optional | Overrides `BINANCE_API_SECRET` env var |
| `--dry-run` | Optional | Validate and print without sending |
| `--json` | Optional | Print raw JSON response |

---

## Assumptions

1. **Testnet only** — the base URL is hardcoded to `https://testnet.binancefuture.com`. Never used with real funds.
2. **Hedge mode is OFF** — all orders use `positionSide=BOTH` (default on new testnet accounts).
3. **LIMIT orders default to GTC** (Good Till Cancelled). This is the most common time-in-force.
4. **Quantity precision** — Binance enforces precision rules per symbol. If you get a filter error, try rounding your quantity to fewer decimal places (e.g., `0.001` instead of `0.0012`).
5. **python-dotenv is optional** — if not installed, credentials must be passed via environment variables or CLI flags.
6. **STOP_MARKET** orders are not supported on the `Binance Futures Testnet` standard endpoint. The bonus order type was implemented in code but cannot be tested on testnet.

---

## Dependencies

```
requests>=2.31.0       # HTTP client
python-dotenv>=1.0.0   # .env file loading (optional but convenient)
```

No Binance-specific SDK is used — all API calls are raw REST requests signed with HMAC-SHA256.

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| Missing API credentials | Clear error message + exit code 1 |
| Invalid symbol/side/type | Validation error before any network call |
| Binance API error (e.g., insufficient balance) | Error code + message displayed |
| Network timeout or connection failure | Friendly error + logged |
| Unexpected exception | Logged with full traceback to file |
