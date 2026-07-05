import { useCallback, useEffect, useState } from "react";

const STORAGE_KEY = "smart-money.watchlist";

function readStored() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

let listeners = new Set();

export function useWatchlist() {
  const [tickers, setTickers] = useState(readStored);

  useEffect(() => {
    const listener = () => setTickers(readStored());
    listeners.add(listener);
    return () => listeners.delete(listener);
  }, []);

  const persist = useCallback((next) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    setTickers(next);
    listeners.forEach((l) => l());
  }, []);

  const isWatched = useCallback((ticker) => tickers.includes(ticker), [tickers]);

  const toggle = useCallback(
    (ticker) => {
      const next = tickers.includes(ticker) ? tickers.filter((t) => t !== ticker) : [...tickers, ticker];
      persist(next);
    },
    [tickers, persist]
  );

  return { tickers, isWatched, toggle };
}
