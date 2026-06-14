"""
client.py
~~~~~~~~~
A thin, reusable wrapper around the Binance Futures Testnet REST API.

Responsibilities
----------------
- Store credentials and base URL
- Sign every private request with HMAC-SHA256
- Send GET / POST requests with timeout + retry logic
- Log every outbound request and inbound response
- Raise clear exceptions on API or network errors
"""

from __future__ import annotations

import hashlib
import hmac
import time
import urllib.parse
from typing import Any
import requests

from bot.error_messages import FRIENDLY_ERRORS
from bot.logging_config import setup_logger

BASE_URL = "https://testnet.binancefuture.com"
RECV_WINDOW = 5000          # ms — tolerance for clock drift
REQUEST_TIMEOUT = 10        # seconds

class BinanceAPIError(Exception):
    """Raised when Binance returns a non-2xx response or an error payload."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        self.friendly = FRIENDLY_ERRORS.get(code, message)
        super().__init__(f"Binance API error {code}: {message}")


class BinanceNetworkError(Exception):
    """Raised on connection/timeout failures."""


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API key and secret must not be empty.")
        self._api_key = api_key
        self._api_secret = api_secret
        self._session = requests.Session()
        self._session.headers.update(
            {
                "X-MBX-APIKEY": self._api_key,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        self._log = setup_logger("trading_bot.client")
        self._log.debug("BinanceClient initialised (testnet).")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _timestamp(self) -> int:
        return int(time.time() * 1000)

    def _sign(self, params: dict) -> dict:
        """Add timestamp + HMAC-SHA256 signature to a params dict."""
        params["timestamp"] = self._timestamp()
        params["recvWindow"] = RECV_WINDOW
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            self._api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _handle_response(self, response: requests.Response) -> Any:
        """Parse JSON and raise BinanceAPIError for error payloads."""
        self._log.debug(
            "Response | status=%s | body=%s",
            response.status_code,
            response.text[:500],   # truncate huge bodies in logs
        )
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            return response.text

        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            raise BinanceAPIError(code=data["code"], message=data.get("msg", "Unknown error"))

        response.raise_for_status()
        return data

    # ------------------------------------------------------------------
    # Public HTTP methods
    # ------------------------------------------------------------------

    def get(self, endpoint: str, params: dict | None = None, signed: bool = False) -> Any:
        params = params or {}
        if signed:
            params = self._sign(params)
        url = BASE_URL + endpoint
        self._log.debug("GET %s | params=%s", url, {k: v for k, v in params.items() if k != "signature"})
        try:
            response = self._session.get(url, params=params, timeout=REQUEST_TIMEOUT)
        except requests.exceptions.Timeout:
            raise BinanceNetworkError(f"GET {endpoint} timed out after {REQUEST_TIMEOUT}s.")
        except requests.exceptions.ConnectionError as exc:
            raise BinanceNetworkError(f"Connection error on GET {endpoint}: {exc}")
        return self._handle_response(response)

    def post(self, endpoint: str, params: dict | None = None, signed: bool = True) -> Any:
        params = params or {}
        if signed:
            params = self._sign(params)
        url = BASE_URL + endpoint
        self._log.debug("POST %s | params=%s", url, {k: v for k, v in params.items() if k != "signature"})
        try:
            response = self._session.post(url, data=params, timeout=REQUEST_TIMEOUT)
        except requests.exceptions.Timeout:
            raise BinanceNetworkError(f"POST {endpoint} timed out after {REQUEST_TIMEOUT}s.")
        except requests.exceptions.ConnectionError as exc:
            raise BinanceNetworkError(f"Connection error on POST {endpoint}: {exc}")
        return self._handle_response(response)

    # ------------------------------------------------------------------
    # Convenience / account helpers
    # ------------------------------------------------------------------

    def ping(self) -> bool:
        """Check connectivity to the Binance Futures Testnet."""
        try:
            self.get("/fapi/v1/ping")
            self._log.info("Ping successful — testnet reachable.")
            return True
        except Exception as exc:
            self._log.error("Ping failed: %s", exc)
            return False

    def get_server_time(self) -> int:
        data = self.get("/fapi/v1/time")
        return data["serverTime"]

    def get_account_info(self) -> dict:
        return self.get("/fapi/v2/account", signed=True)

    def get_exchange_info(self, symbol: str) -> dict:
        return self.get("/fapi/v1/exchangeInfo", params={"symbol": symbol})
