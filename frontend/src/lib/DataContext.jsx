import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api, API_BASE } from "./api";

const DataContext = createContext(null);

export function DataProvider({ children }) {
  const [conviction, setConviction] = useState(null);
  const [polymarket, setPolymarket] = useState(null);
  const [insiders, setInsiders] = useState(null);
  const [congress, setCongress] = useState(null);
  const [meta, setMeta] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const loadAll = useCallback(async () => {
    setError(null);
    const [convictionRes, polymarketRes, insidersRes, congressRes, metaRes] = await Promise.allSettled([
      api.conviction(),
      api.polymarket(),
      api.insiders(false),
      api.congress(),
      api.meta(),
    ]);

    if (convictionRes.status === "fulfilled") setConviction(convictionRes.value);
    if (polymarketRes.status === "fulfilled") setPolymarket(polymarketRes.value);
    if (insidersRes.status === "fulfilled") setInsiders(insidersRes.value);
    if (congressRes.status === "fulfilled") setCongress(congressRes.value);
    if (metaRes.status === "fulfilled") setMeta(metaRes.value);

    const failed = [convictionRes, polymarketRes, insidersRes, congressRes].filter((r) => r.status === "rejected");
    if (failed.length) {
      const reason = failed[0].reason?.message || String(failed[0].reason);
      setError(`Couldn't reach the data API at ${API_BASE} — ${reason}`);
    }
  }, []);

  useEffect(() => {
    setLoading(true);
    loadAll().finally(() => setLoading(false));
  }, [loadAll]);

  const refresh = useCallback(async () => {
    setRefreshing(true);
    try {
      await api.refresh();
    } catch {
      // backend refresh endpoint failed; still try to reload whatever is cached
    }
    await loadAll();
    setRefreshing(false);
  }, [loadAll]);

  const metaBySource = useMemo(() => {
    const map = {};
    (meta || []).forEach((m) => {
      map[m.source] = m;
    });
    return map;
  }, [meta]);

  const value = {
    conviction,
    polymarket,
    insiders,
    congress,
    meta: metaBySource,
    loading,
    refreshing,
    error,
    refresh,
  };

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
}

export function useData() {
  const ctx = useContext(DataContext);
  if (!ctx) throw new Error("useData must be used within DataProvider");
  return ctx;
}
