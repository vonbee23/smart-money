import { Outlet } from "react-router-dom";
import BottomNav from "./BottomNav";
import Footer from "./Footer";
import Header from "./Header";

export default function Layout() {
  return (
    <div className="mx-auto flex h-dvh max-w-lg flex-col bg-bg">
      <Header />
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
      <Footer />
      <BottomNav />
    </div>
  );
}
