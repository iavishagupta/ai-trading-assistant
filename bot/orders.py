"""
orders.py
~~~~~~~~~
All order-placement logic.  The CLI layer calls these functions;
they call BinanceClient and return structured result dicts.

Supported order types
---------------------
MARKET      — execute immediately at best available price
LIMIT       — execute only when price reaches a target level
STOP_MARKET — trigger a market order when price hits a stop level (bonus)
"""

from __future__ import annotations

from typing import Any

from bot.client import BinanceClient, BinanceAPIError, BinanceNetworkError
from bot.logging_config import setup_logger

_log = setup_logger("trading_bot.orders")

ENDPOINT = "/fapi/v1/order"


def _build_result(raw: dict) -> dict:
    """
    Normalise Binance order response into a clean summary dict.
    All fields we care about are always present; extras are kept under 'raw'.
    """
    return {
        "orderId": raw.get("orderId"),
        "symbol": raw.get("symbol"),
        "side": raw.get("side"),
        "type": raw.get("type"),
        "status": raw.get("status"),
        "origQty": raw.get("origQty"),
        "executedQty": raw.get("executedQty"),
        "avgPrice": raw.get("avgPrice"),
        "price": raw.get("price"),
        "stopPrice": raw.get("stopPrice"),
        "timeInForce": raw.get("timeInForce"),
        "updateTime": raw.get("updateTime"),
        "raw": raw,
    }


def place_market_order(
    client: BinanceClient,
    *,
    symbol: str,
    side: str,
    quantity: float,
) -> dict:
    """
    Place a MARKET order.

    Parameters
    ----------
    client   : authenticated BinanceClient
    symbol   : e.g. "BTCUSDT"
    side     : "BUY" or "SELL"
    quantity : amount of base asset to trade
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
    }
    _log.info(
        "Placing MARKET %s order | symbol=%s | qty=%s",
        side, symbol, quantity,
    )
    try:
        raw = client.post(ENDPOINT, params=params, signed=True)
        result = _build_result(raw)
        _log.info(
            "MARKET order placed | orderId=%s | status=%s | executedQty=%s | avgPrice=%s",
            result["orderId"], result["status"], result["executedQty"], result["avgPrice"],
        )
        return result
    except BinanceAPIError as exc:
        _log.error("MARKET order failed (API) | code=%s | msg=%s", exc.code, exc.message)
        raise
    except BinanceNetworkError as exc:
        _log.error("MARKET order failed (network) | %s", exc)
        raise


def place_limit_order(
    client: BinanceClient,
    *,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:
    """
    Place a LIMIT order.

    Parameters
    ----------
    client        : authenticated BinanceClient
    symbol        : e.g. "BTCUSDT"
    side          : "BUY" or "SELL"
    quantity      : amount of base asset to trade
    price         : limit price
    time_in_force : GTC (Good Till Cancel) | IOC | FOK
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": time_in_force,
    }
    _log.info(
        "Placing LIMIT %s order | symbol=%s | qty=%s | price=%s | TIF=%s",
        side, symbol, quantity, price, time_in_force,
    )
    try:
        raw = client.post(ENDPOINT, params=params, signed=True)
        result = _build_result(raw)
        _log.info(
            "LIMIT order placed | orderId=%s | status=%s | price=%s | executedQty=%s",
            result["orderId"], result["status"], result["price"], result["executedQty"],
        )
        return result
    except BinanceAPIError as exc:
        _log.error("LIMIT order failed (API) | code=%s | msg=%s", exc.code, exc.message)
        raise
    except BinanceNetworkError as exc:
        _log.error("LIMIT order failed (network) | %s", exc)
        raise


def place_stop_market_order(
    client: BinanceClient,
    *,
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
) -> dict:
    """
    Place a STOP_MARKET order (bonus order type).

    A stop-market becomes a market order once price crosses `stop_price`.
    Useful for stop-losses and breakout entries.

    Parameters
    ----------
    client     : authenticated BinanceClient
    symbol     : e.g. "BTCUSDT"
    side       : "BUY" or "SELL"
    quantity   : amount of base asset to trade
    stop_price : price level that triggers the order
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "STOP_MARKET",
        "quantity": quantity,
        "stopPrice": stop_price,
    }
    _log.info(
        "Placing STOP_MARKET %s order | symbol=%s | qty=%s | stopPrice=%s",
        side, symbol, quantity, stop_price,
    )
    try:
        raw = client.post(ENDPOINT, params=params, signed=True)
        result = _build_result(raw)
        _log.info(
            "STOP_MARKET order placed | orderId=%s | status=%s | stopPrice=%s",
            result["orderId"], result["status"], result["stopPrice"],
        )
        return result
    except BinanceAPIError as exc:
        _log.error("STOP_MARKET order failed (API) | code=%s | msg=%s", exc.code, exc.message)
        raise
    except BinanceNetworkError as exc:
        _log.error("STOP_MARKET order failed (network) | %s", exc)
        raise


def place_order(client: BinanceClient, *, validated_params: dict) -> dict:
    """
    Dispatcher — routes to the correct placement function based on order_type.
    Accepts the dict returned by validators.validate_all().
    """
    order_type = validated_params["order_type"]

    if order_type == "MARKET":
        return place_market_order(
            client,
            symbol=validated_params["symbol"],
            side=validated_params["side"],
            quantity=validated_params["quantity"],
        )
    elif order_type == "LIMIT":
        return place_limit_order(
            client,
            symbol=validated_params["symbol"],
            side=validated_params["side"],
            quantity=validated_params["quantity"],
            price=validated_params["price"],
        )
    elif order_type == "STOP_MARKET":
        return place_stop_market_order(
            client,
            symbol=validated_params["symbol"],
            side=validated_params["side"],
            quantity=validated_params["quantity"],
            stop_price=validated_params["stop_price"],
        )
    else:
        raise ValueError(f"Unsupported order type: {order_type}")
