"""Keyword -> ticker map used to heuristically link a Polymarket market's
question text to a stock ticker, since Polymarket has no ticker field.
Longer/more specific keys are matched first to avoid collisions
(e.g. "Meta Platforms" before "Meta").
"""

COMPANY_TICKERS: dict[str, str] = {
    "nvidia": "NVDA",
    "tesla": "TSLA",
    "apple": "AAPL",
    "microsoft": "MSFT",
    "meta platforms": "META",
    "facebook": "META",
    "amazon": "AMZN",
    "alphabet": "GOOGL",
    "google": "GOOGL",
    "advanced micro devices": "AMD",
    "netflix": "NFLX",
    "palantir": "PLTR",
    "coinbase": "COIN",
    "jpmorgan": "JPM",
    "exxon": "XOM",
    "boeing": "BA",
    "disney": "DIS",
    "unitedhealth": "UNH",
    "pfizer": "PFE",
    "intel": "INTC",
    "salesforce": "CRM",
    "shopify": "SHOP",
    "berkshire": "BRK.B",
    "oracle": "ORCL",
    "broadcom": "AVGO",
    "qualcomm": "QCOM",
    "starbucks": "SBUX",
    "airbnb": "ABNB",
    "uber": "UBER",
    "gamestop": "GME",
    "amc entertainment": "AMC",
    "moderna": "MRNA",
    "ford": "F",
    "general motors": "GM",
}


def match_tickers(text: str) -> list[str]:
    lowered = text.lower()
    found: set[str] = set()
    for keyword, ticker in COMPANY_TICKERS.items():
        if keyword in lowered:
            found.add(ticker)
    return sorted(found)


TICKER_COMPANY: dict[str, str] = {
    "NVDA": "NVIDIA Corporation",
    "TSLA": "Tesla, Inc.",
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "META": "Meta Platforms, Inc.",
    "AMZN": "Amazon.com, Inc.",
    "GOOGL": "Alphabet Inc.",
    "GOOG": "Alphabet Inc.",
    "AMD": "Advanced Micro Devices, Inc.",
    "NFLX": "Netflix, Inc.",
    "PLTR": "Palantir Technologies Inc.",
    "COIN": "Coinbase Global, Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "XOM": "Exxon Mobil Corporation",
    "BA": "The Boeing Company",
    "DIS": "The Walt Disney Company",
    "UNH": "UnitedHealth Group Incorporated",
    "PFE": "Pfizer Inc.",
    "INTC": "Intel Corporation",
    "CRM": "Salesforce, Inc.",
    "SHOP": "Shopify Inc.",
}


def company_name(ticker: str, fallback: str = "") -> str:
    return TICKER_COMPANY.get(ticker.upper(), fallback or ticker.upper())
