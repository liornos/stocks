<<<<<<< HEAD
# Stocks Reader

Small Python utility for fetching stock quotes and historical data using Yahoo Finance.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Fetch the latest quote for a ticker:

```bash
python main.py AAPL
```

Fetch quotes for several tickers in one run (comma-separated or space-separated):

```bash
python main.py NVDA AAPL MSFT AMZN GOOGL META BRK.B AVGO TSLA JPM
```

Fetch the latest quote and save it to `stocks_reader.json`:

```bash
python main.py AAPL --json-output
```

Fetch the latest quote and the last month of daily candles, writing to CSV:

```bash
python main.py MSFT --history --period 1mo --interval 1d --output msft.csv
```

If no `--output` is provided, the historical data prints to the console.

> Note: Historical data retrieval (`--history`) is only available when requesting a single ticker.

=======
# Stocks Reader

Small Python utility for fetching stock quotes and historical data using Yahoo Finance.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Fetch the latest quote for a ticker:

```bash
python main.py AAPL
```

Fetch quotes for several tickers in one run (comma-separated or space-separated):

```bash
python main.py NVDA AAPL MSFT AMZN GOOGL META BRK.B AVGO TSLA JPM
```

Fetch the latest quote and save it to `stocks_reader.json`:

```bash
python main.py AAPL --json-output
```

Fetch the latest quote and the last month of daily candles, writing to CSV:

```bash
python main.py MSFT --history --period 1mo --interval 1d --output msft.csv
```

If no `--output` is provided, the historical data prints to the console.

> Note: Historical data retrieval (`--history`) is only available when requesting a single ticker.

>>>>>>> bdf42e3a6767d6ff9f603e87431992fedf905d66
