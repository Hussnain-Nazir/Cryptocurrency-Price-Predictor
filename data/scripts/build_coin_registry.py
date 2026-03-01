"""
CryptoVision — data/scripts/build_coin_registry.py

Fetches the top coins by market cap from the CoinGecko public API,
cleans the results, and saves them to data/raw/coin_registry.csv.

Usage:
    python data/scripts/build_coin_registry.py

The script limits output to ~1,000 coins to cover all mainstream assets
while excluding obscure or defunct tokens.
"""

import sys
import os
import time
import requests
import pandas as pd

# Configuration
COINGECKO_MARKETS_URL = "https://api.coingecko.com/api/v3/coins/markets"
TARGET_COIN_COUNT     = 1000
COINS_PER_PAGE        = 250      # CoinGecko max per request
RATE_LIMIT_SLEEP      = 1.5      # seconds between requests (free tier)
RATE_LIMIT_RETRY      = 65       # seconds to wait on HTTP 429
MAX_RETRIES           = 3

OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "..", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "coin_registry.csv")


# Helpers
def _page_count(total: int, per_page: int) -> int:
    return (total + per_page - 1) // per_page


def _fetch_page(page_number: int) -> list[dict]:
    """
    Request one page of market data from CoinGecko and return a list of
    {'ticker': 'BTC-USD', 'name': 'Bitcoin'} dicts.
    """
    params = {
        "vs_currency": "usd",
        "order":       "market_cap_desc",
        "per_page":    COINS_PER_PAGE,
        "page":        page_number,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                COINGECKO_MARKETS_URL, params=params, timeout=20
            )
            response.raise_for_status()

            coins = response.json()
            if not coins:
                return []

            return [
                {
                    "ticker": f"{coin['symbol'].upper()}-USD",
                    "name":   coin["name"],
                }
                for coin in coins
            ]

        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response else 0
            if status == 429:
                print(
                    f"    Rate limit hit on page {page_number}. "
                    f"Retrying in {RATE_LIMIT_RETRY}s …"
                )
                time.sleep(RATE_LIMIT_RETRY)
            else:
                print(f"    HTTP error {status} on page {page_number}: {exc}")
                return []
        except requests.RequestException as exc:
            print(f"    Network error on page {page_number} (attempt {attempt}): {exc}")
            if attempt < MAX_RETRIES:
                time.sleep(5)

    print(f"    Giving up on page {page_number} after {MAX_RETRIES} attempts.")
    return []


# Main
def build_registry() -> pd.DataFrame:
    total_pages = _page_count(TARGET_COIN_COUNT, COINS_PER_PAGE)
    all_rows: list[dict] = []

    print(f"Fetching {TARGET_COIN_COUNT} coins across {total_pages} page(s) …\n")

    for page in range(1, total_pages + 1):
        print(f"  Page {page}/{total_pages} … ", end="", flush=True)
        rows = _fetch_page(page)
        all_rows.extend(rows)
        print(f"{len(rows)} coins retrieved  (total so far: {len(all_rows)})")

        if len(all_rows) >= TARGET_COIN_COUNT:
            break

        if page < total_pages:
            time.sleep(RATE_LIMIT_SLEEP)

    # Deduplicate on ticker symbol
    df = (
        pd.DataFrame(all_rows)
        .drop_duplicates(subset="ticker")
        .iloc[:TARGET_COIN_COUNT]
        .reset_index(drop=True)
    )

    # Persist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✓ Registry saved to '{OUTPUT_FILE}'  ({len(df)} coins)\n")
    print(df.head(10).to_string(index=False))
    return df


if __name__ == "__main__":
    build_registry()
