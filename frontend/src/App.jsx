import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import { DataProvider } from "./lib/DataContext";
import CongressPage from "./pages/CongressPage";
import ConvictionPage from "./pages/ConvictionPage";
import InsidersPage from "./pages/InsidersPage";
import MarketDetailPage from "./pages/MarketDetailPage";
import PolymarketPage from "./pages/PolymarketPage";
import TickerDetailPage from "./pages/TickerDetailPage";
import WatchlistPage from "./pages/WatchlistPage";

export default function App() {
  return (
    <DataProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<ConvictionPage />} />
            <Route path="ticker/:ticker" element={<TickerDetailPage />} />
            <Route path="polymarket" element={<PolymarketPage />} />
            <Route path="polymarket/:id" element={<MarketDetailPage />} />
            <Route path="insiders" element={<InsidersPage />} />
            <Route path="congress" element={<CongressPage />} />
            <Route path="watchlist" element={<WatchlistPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </DataProvider>
  );
}
