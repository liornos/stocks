"""
High-level utilities to retrieve stock price data from Yahoo Finance.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

try:
    import yfinance as yf  # type: ignore
except ImportError as exc:  # pragma: no cover - exercised when yfinance missing
    yf = None  # type: ignore[assignment]
    _YFINANCE_IMPORT_ERROR = exc
else:
    _YFINANCE_IMPORT_ERROR = None

@dataclass(frozen=True)
class StockQuote:
    """Represents a single stock quote snapshot."""

    symbol: str
    price: float
    currency: str
    time: datetime


class StockDataFetcher:
    """
    Fetches stock price data from Yahoo Finance using the yfinance library.
    """

    def __init__(self, symbol: str) -> None:
        if not symbol:
            raise ValueError("symbol must be a non-empty string")
        if yf is None:
            raise ImportError(
                "The 'yfinance' package is required. Install it via 'pip install yfinance'."
            ) from _YFINANCE_IMPORT_ERROR

        self._symbol = symbol.upper()
        self._ticker = yf.Ticker(self._symbol)

    @property
    def symbol(self) -> str:
        return self._symbol

    def latest_quote(self) -> StockQuote:
        """
        Retrieves the latest quote for the ticker.

        Returns:
            StockQuote: The latest price information.
        """
        info = self._ticker.fast_info

        last_price: Optional[float] = info.get("lastPrice") or info.get("last_price")
        currency: Optional[str] = info.get("currency")
        last_trade_date: Optional[int] = info.get("lastTradeDate")

        if last_price is not None and currency and last_trade_date:
            quote_time = datetime.fromtimestamp(last_trade_date)
            return StockQuote(
                symbol=self._symbol,
                price=float(last_price),
                currency=currency,
                time=quote_time,
            )

        history_df = self._ticker.history(period="5d", interval="1d")
        if history_df.empty:
            history_df = self._ticker.history(period="1d", interval="1m")

        if history_df.empty:
            raise RuntimeError(
                f"Unable to retrieve latest quote for symbol {self._symbol}"
            )

        last_row = history_df.iloc[-1]
        last_index = history_df.index[-1]

        fallback_currency: Optional[str] = currency
        if not fallback_currency:
            try:
                ticker_info = self._ticker.info
            except Exception:  # pragma: no cover - network / upstream errors
                ticker_info = {}
            fallback_currency = ticker_info.get("currency")

        if fallback_currency is None:
            raise RuntimeError(
                f"Unable to retrieve currency for symbol {self._symbol}"
            )

        quote_time = (
            last_index.to_pydatetime()
            if hasattr(last_index, "to_pydatetime")
            else datetime.now()
        )

        return StockQuote(
            symbol=self._symbol,
            price=float(last_row["Close"]),
            currency=fallback_currency,
            time=quote_time,
        )

    def history(
        self,
        period: str = "1mo",
        interval: str = "1d",
    ):
        """
        Retrieves historical data for the ticker.

        Args:
            period: Total length of time to download (e.g. '1d', '5d', '1mo', '1y').
            interval: Data interval (e.g. '1m', '2m', '5m', '1h', '1d', '1wk').

        Returns:
            pandas.DataFrame: Historical OHLC data indexed by datetime.
        """
        data = self._ticker.history(period=period, interval=interval)
        if data.empty:
            raise RuntimeError(
                f"No historical data returned for symbol {self._symbol}"
            )
        return data

