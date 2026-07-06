import { NavLink, Outlet } from "react-router-dom";
import { BarChart3, Bot, FileText, Home, ShieldCheck } from "lucide-react";

const navItems = [
  { label: "Dashboard", path: "/", icon: Home },
  { label: "Ask HR", path: "/chat", icon: Bot },
  { label: "Policy Documents", path: "/documents", icon: FileText },
  { label: "Analytics", path: "/analytics", icon: BarChart3 }
];

export default function Layout() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-slate-800 bg-slate-950 px-5 py-6 shadow-2xl shadow-black/30 lg:block">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500 text-white shadow-lg shadow-blue-500/25">
            <ShieldCheck size={22} />
          </div>
          <div>
            <div className="text-base font-semibold text-white">HR Policy Copilot</div>
            <div className="text-xs text-slate-400">Employee Knowledge Assistant</div>
          </div>
        </div>
        <nav className="mt-9 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition ${
                  isActive
                    ? "bg-blue-500/15 text-blue-300 ring-1 ring-blue-500/25"
                    : "text-slate-400 hover:bg-slate-900 hover:text-slate-100"
                }`
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="absolute bottom-6 left-5 right-5 rounded-lg border border-slate-800 bg-slate-900/80 p-4">
          <div className="text-sm font-semibold text-white">Grounded HR answers</div>
          <p className="mt-1 text-xs leading-5 text-slate-400">
            Responses are generated from approved policy documents with citations and confidence scoring.
          </p>
        </div>
      </aside>
      <div className="lg:pl-72">
        <header className="sticky top-0 z-10 border-b border-slate-800 bg-slate-950/90 px-5 py-4 backdrop-blur">
          <div className="mx-auto flex max-w-7xl items-center justify-between">
            <div>
              <div className="text-sm text-slate-400">People Operations</div>
              <div className="text-lg font-semibold text-white">Employee HR Assistant</div>
            </div>
            <div className="rounded-full border border-slate-700 bg-slate-900 px-3 py-1 text-xs font-medium text-slate-300">
              View-only policy library
            </div>
          </div>
        </header>
        <main className="mx-auto max-w-7xl px-5 py-7">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
