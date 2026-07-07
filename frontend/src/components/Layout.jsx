import { Outlet } from "react-router-dom";
import { useData } from "../lib/DataContext";
import BottomNav from "./BottomNav";
import Footer from "./Footer";
import Header from "./Header";

export default function Layout() {
  const { error } = useData();

  return (
    <div className="mx-auto flex h-dvh max-w-lg flex-col bg-bg">
      <Header />
      {error && (
        <p className="border-b border-bear-dim bg-bear-dim/40 px-4 py-2 text-xs leading-snug text-bear">
          {error}
        </p>
      )}
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
      <Footer />
      <BottomNav />
    </div>
  );
}
