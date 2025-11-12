<<<<<<< HEAD
"""
Command-line entry point for fetching stock quotes and historical data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from stocks_reader import StockDataFetcher


def _normalize_symbols(raw_symbols: list[str]) -> list[str]:
    symbols: list[str] = []
    for item in raw_symbols:
        parts = [part.strip().upper() for part in item.split(",")]
        symbols.extend(part for part in parts if part)
    return symbols


def _retrieve_quote(symbol: str) -> tuple[dict, StockDataFetcher]:
    candidates = []
    upper_symbol = symbol.upper()
    candidates.append(upper_symbol)
    if "." in upper_symbol and "-" not in upper_symbol:
        candidates.append(upper_symbol.replace(".", "-"))

    last_error: Exception | None = None
    for candidate in dict.fromkeys(candidates):  # preserve order, remove duplicates
        try:
            fetcher = StockDataFetcher(candidate)
            quote = fetcher.latest_quote()
            payload = {
                "symbol": upper_symbol,
                "price": quote.price,
                "currency": quote.currency,
                "time": quote.time.isoformat(),
            }
            return payload, fetcher
        except Exception as exc:  # noqa: BLE001 - surface last error to caller
            last_error = exc

    raise RuntimeError(
        f"Unable to retrieve latest quote for symbol {upper_symbol}"
    ) from last_error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch stock price information from Yahoo Finance."
    )
    parser.add_argument(
        "symbols",
        nargs="+",
        help=(
            "Ticker symbol(s) to fetch (e.g. AAPL or 'NVDA AAPL MSFT'). "
            "Comma-separated values are also supported."
        ),
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Fetch historical OHLC data in addition to the latest quote.",
    )
    parser.add_argument(
        "--period",
        default="1mo",
        help="Period for historical data (default: 1mo).",
    )
    parser.add_argument(
        "--interval",
        default="1d",
        help="Interval for historical data (default: 1d).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write historical data as CSV.",
    )
    parser.add_argument(
        "--json-output",
        nargs="?",
        const=Path("stocks_reader.json"),
        type=Path,
        help=(
            "Write latest quote JSON to file. "
            "If no path is provided, saves to 'stocks_reader.json'."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    symbols = _normalize_symbols(args.symbols)
    if not symbols:
        raise SystemExit("At least one symbol must be provided.")

    if args.history and len(symbols) > 1:
        raise SystemExit(
            "Historical data retrieval is only supported when fetching a single symbol."
        )

    if len(symbols) == 1:
        payload, fetcher = _retrieve_quote(symbols[0])
        pretty_payload = json.dumps(payload, indent=2)
        print(pretty_payload)

        if args.json_output:
            output_path = args.json_output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(pretty_payload + "\n", encoding="utf-8")
            print(f"Latest quote saved to {output_path}")

        if args.history:
            history_df = fetcher.history(period=args.period, interval=args.interval)
            if args.output:
                history_df.to_csv(args.output)
                print(f"Historical data written to {args.output}")
            else:
                print(history_df.tail())
        return

    quotes_payload = []
    for symbol in symbols:
        payload, _ = _retrieve_quote(symbol)
        quotes_payload.append(payload)

    pretty_payload = json.dumps(quotes_payload, indent=2)
    print(pretty_payload)

    if args.json_output:
        output_path = args.json_output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(pretty_payload + "\n", encoding="utf-8")
        print(f"Latest quotes saved to {output_path}")


if __name__ == "__main__":
    main()

=======
"""
Command-line entry point for fetching stock quotes and historical data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from stocks_reader import StockDataFetcher


def _normalize_symbols(raw_symbols: list[str]) -> list[str]:
    symbols: list[str] = []
    for item in raw_symbols:
        parts = [part.strip().upper() for part in item.split(",")]
        symbols.extend(part for part in parts if part)
    return symbols


def _retrieve_quote(symbol: str) -> tuple[dict, StockDataFetcher]:
    candidates = []
    upper_symbol = symbol.upper()
    candidates.append(upper_symbol)
    if "." in upper_symbol and "-" not in upper_symbol:
        candidates.append(upper_symbol.replace(".", "-"))

    last_error: Exception | None = None
    for candidate in dict.fromkeys(candidates):  # preserve order, remove duplicates
        try:
            fetcher = StockDataFetcher(candidate)
            quote = fetcher.latest_quote()
            payload = {
                "symbol": upper_symbol,
                "price": quote.price,
                "currency": quote.currency,
                "time": quote.time.isoformat(),
            }
            return payload, fetcher
        except Exception as exc:  # noqa: BLE001 - surface last error to caller
            last_error = exc

    raise RuntimeError(
        f"Unable to retrieve latest quote for symbol {upper_symbol}"
    ) from last_error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch stock price information from Yahoo Finance."
    )
    parser.add_argument(
        "symbols",
        nargs="+",
        help=(
            "Ticker symbol(s) to fetch (e.g. AAPL or 'NVDA AAPL MSFT'). "
            "Comma-separated values are also supported."
        ),
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Fetch historical OHLC data in addition to the latest quote.",
    )
    parser.add_argument(
        "--period",
        default="1mo",
        help="Period for historical data (default: 1mo).",
    )
    parser.add_argument(
        "--interval",
        default="1d",
        help="Interval for historical data (default: 1d).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write historical data as CSV.",
    )
    parser.add_argument(
        "--json-output",
        nargs="?",
        const=Path("stocks_reader.json"),
        type=Path,
        help=(
            "Write latest quote JSON to file. "
            "If no path is provided, saves to 'stocks_reader.json'."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    symbols = _normalize_symbols(args.symbols)
    if not symbols:
        raise SystemExit("At least one symbol must be provided.")

    if args.history and len(symbols) > 1:
        raise SystemExit(
            "Historical data retrieval is only supported when fetching a single symbol."
        )

    if len(symbols) == 1:
        payload, fetcher = _retrieve_quote(symbols[0])
        pretty_payload = json.dumps(payload, indent=2)
        print(pretty_payload)

        if args.json_output:
            output_path = args.json_output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(pretty_payload + "\n", encoding="utf-8")
            print(f"Latest quote saved to {output_path}")

        if args.history:
            history_df = fetcher.history(period=args.period, interval=args.interval)
            if args.output:
                history_df.to_csv(args.output)
                print(f"Historical data written to {args.output}")
            else:
                print(history_df.tail())
        return

    quotes_payload = []
    for symbol in symbols:
        payload, _ = _retrieve_quote(symbol)
        quotes_payload.append(payload)

    pretty_payload = json.dumps(quotes_payload, indent=2)
    print(pretty_payload)

    if args.json_output:
        output_path = args.json_output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(pretty_payload + "\n", encoding="utf-8")
        print(f"Latest quotes saved to {output_path}")


if __name__ == "__main__":
    main()

>>>>>>> bdf42e3a6767d6ff9f603e87431992fedf905d66
