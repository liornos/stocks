"""
Stocks reader package providing utilities to retrieve equity price data.
"""

from .fetcher import StockDataFetcher, StockQuote

__all__ = ["StockDataFetcher", "StockQuote"]

