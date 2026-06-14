#!/usr/bin/env python3
"""
cli.py
~~~~~~
Command-line entry point for the Binance Futures Testnet Trading Bot.

Usage examples
--------------
# Market BUY
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Limit SELL
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 100000

# Stop-Market BUY (bonus order type)
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.01 --stop-price 95000

Environment variables (or .env file)
-------------------------------------
BINANCE_API_KEY    — your testnet API key
BINANCE_API_SECRET — your testnet API secret
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# Load .env if python-dotenv is installed (optional convenience)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from bot.client import BinanceClient, BinanceAPIError, BinanceNetworkError
from bot.logging_config import setup_logger
from bot.orders import place_order
from bot.validators import validate_all, ValidationError

_log = setup_logger("trading_bot.cli")

# ── ANSI colours (disabled automatically on Windows without ANSI support) ──────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def _banner() -> None:
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════╗
║   Binance Futures Testnet — Trading Bot      ║
╚══════════════════════════════════════════════╝{RESET}
""")


def _print_request_summary(params: dict) -> None:
    print(f"{BOLD}── Order Request ──────────────────────────────{RESET}")
    print(f"  Symbol     : {params['symbol']}")
    print(f"  Side       : {params['side']}")
    print(f"  Type       : {params['order_type']}")
    print(f"  Quantity   : {params['quantity']}")
    if params.get("price"):
        print(f"  Price      : {params['price']}")
    if params.get("stop_price"):
        print(f"  Stop Price : {params['stop_price']}")
    print()


def _print_order_result(result: dict) -> None:
    print(f"{BOLD}── Order Response ─────────────────────────────{RESET}")
    print(f"  Order ID      : {result['orderId']}")
    print(f"  Status        : {result['status']}")
    print(f"  Executed Qty  : {result['executedQty']}")
    if result.get("avgPrice") and float(result["avgPrice"] or 0) > 0:
        print(f"  Avg Price     : {result['avgPrice']}")
    if result.get("price") and float(result["price"] or 0) > 0:
        print(f"  Limit Price   : {result['price']}")
    if result.get("stopPrice") and float(result["stopPrice"] or 0) > 0:
        print(f"  Stop Price    : {result['stopPrice']}")
    if result.get("timeInForce"):
        print(f"  Time In Force : {result['timeInForce']}")
    print()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --symbol BTCUSDT --side BUY  --type MARKET     --quantity 0.01
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT       --quantity 0.01 --price 100000
  python cli.py --symbol BTCUSDT --side BUY  --type STOP_MARKET --quantity 0.01 --stop-price 95000
        """,
    )
    parser.add_argument("--symbol",     required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  help="BUY or SELL")
    parser.add_argument("--type",       required=True,  dest="order_type",
                        help="MARKET | LIMIT | STOP_MARKET")
    parser.add_argument("--quantity",   required=True,  type=float,
                        help="Amount of base asset to trade")
    parser.add_argument("--price",      required=False, type=float, default=None,
                        help="Limit price (required for LIMIT orders)")
    parser.add_argument("--stop-price", required=False, type=float, default=None,
                        dest="stop_price",
                        help="Stop trigger price (required for STOP_MARKET orders)")
    parser.add_argument("--api-key",    required=False, default=None,
                        help="Binance API key (overrides BINANCE_API_KEY env var)")
    parser.add_argument("--api-secret", required=False, default=None,
                        help="Binance API secret (overrides BINANCE_API_SECRET env var)")
    parser.add_argument("--dry-run",    action="store_true",
                        help="Validate and print the request without sending it")
    parser.add_argument("--json",       action="store_true", dest="json_output",
                        help="Print the raw order response as JSON")
    return parser


def main() -> None:
    _banner()
    parser = _build_parser()
    args = parser.parse_args()

    # ── Resolve credentials ────────────────────────────────────────────────────
    api_key    = args.api_key    or os.environ.get("BINANCE_API_KEY",    "")
    api_secret = args.api_secret or os.environ.get("BINANCE_API_SECRET", "")

    if not api_key or not api_secret:
        _log.error("API credentials missing. Set BINANCE_API_KEY and BINANCE_API_SECRET.")
        print(
            f"{RED}✖  API credentials not found.\n"
            f"   Set them via environment variables or pass --api-key / --api-secret.{RESET}"
        )
        sys.exit(1)

    # ── Validate inputs ────────────────────────────────────────────────────────
    try:
        validated = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValidationError as exc:
        _log.warning("Input validation failed: %s", exc)
        print(f"{RED}✖  Validation error: {exc}{RESET}")
        sys.exit(1)

    _print_request_summary(validated)

    if args.dry_run:
        print(f"{YELLOW}ℹ  Dry-run mode — no order was sent.{RESET}")
        _log.info("Dry-run mode active. Order was NOT sent.")
        sys.exit(0)

    # ── Initialise client and ping testnet ─────────────────────────────────────
    try:
        client = BinanceClient(api_key=api_key, api_secret=api_secret)
    except ValueError as exc:
        _log.error("Client init failed: %s", exc)
        print(f"{RED}✖  {exc}{RESET}")
        sys.exit(1)

    if not client.ping():
        print(f"{RED}✖  Cannot reach Binance Futures Testnet. Check your internet connection.{RESET}")
        sys.exit(1)

    # ── Place the order ────────────────────────────────────────────────────────
    try:
        result = place_order(client, validated_params=validated)
    except ValidationError as exc:
        _log.warning("Order validation error: %s", exc)
        print(f"{RED}✖  Validation error: {exc}{RESET}")
        sys.exit(1)
    except BinanceAPIError as exc:
        print(f"{RED}✖  Binance API error [{exc.code}]: {exc.message}{RESET}")
        sys.exit(1)
    except BinanceNetworkError as exc:
        print(f"{RED}✖  Network error: {exc}{RESET}")
        sys.exit(1)
    except Exception as exc:
        _log.exception("Unexpected error: %s", exc)
        print(f"{RED}✖  Unexpected error: {exc}{RESET}")
        sys.exit(1)

    # ── Display result ─────────────────────────────────────────────────────────
    if args.json_output:
        print(json.dumps(result["raw"], indent=2))
    else:
        _print_order_result(result)
        print(f"{GREEN}{BOLD}✔  Order placed successfully!{RESET}")

    _log.info("CLI session complete.")


if __name__ == "__main__":
    main()
