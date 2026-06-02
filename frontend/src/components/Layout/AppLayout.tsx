import { Outlet } from "react-router-dom";
import { Sidebar } from "../Sidebar/Sidebar";

export function AppLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-bg-base">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Outlet />
      </main>
    </div>
  );
}
