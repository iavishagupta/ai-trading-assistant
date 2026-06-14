"""
error_messages.py
~~~~~~~~~~~~~~~~~
User-friendly error messages for Binance API error codes.
"""

FRIENDLY_ERRORS = {
    # Order size errors
    -4164: "Order value too small. Minimum order value is 5 USD. For low-price coins like ROSE (\~0.006 USD), you need at least 800+ units to meet this requirement.",
    -4003: "Quantity too small. Please increase your order size.",
    -1013: "Price or quantity is outside the allowed range for this symbol.",

    # Price errors
    -4010: "Invalid price. Please check the price you entered.",
    -4016: "Price exceeds the allowed range for this symbol on testnet.",

    # Order type/side errors
    -4061: "Order side is invalid. Must be BUY or SELL.",
    -4062: "Invalid order type. Supported types are MARKET and LIMIT.",
    -1111: "Precision too high. Try rounding your quantity to fewer decimal places.",

    # Auth errors
    -2015: "Invalid API key or secret. Please check your credentials.",
    -2014: "Invalid API key format. Please regenerate your testnet keys.",
    -1022: "Invalid signature. Your API secret may be incorrect.",

    # Account errors
    -2019: "Insufficient margin balance to place this order.",
    -3045: "Account has no open positions to close.",

    # Input errors
    -1121: "Invalid trading symbol. Please check the coin name.",
    -1100: "Invalid order parameters. Please check your inputs.",
    -1102: "Missing required parameter. Please check your order details.",
    -1106: "Parameter not required for this order type.",

    # Rate limit / server errors
    -1003: "Too many requests. Please wait a moment before trying again.",
    -1001: "Binance server timeout. Please try again.",
    -1007: "Binance server busy. Please try again in a moment.",
}