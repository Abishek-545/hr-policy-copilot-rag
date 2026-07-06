import { Link } from "react-router-dom";
import { ArrowRight, Clock, FileText, MessageSquareText, ShieldCheck } from "lucide-react";

const questions = [
  "How many vacation days do employees receive?",
  "What is the remote work policy?",
  "How do I request sick leave?",
  "What expenses are reimbursable?",
  "What is the probation period?",
  "How do I report workplace concerns?"
];

export default function Dashboard() {
  return (
    <div className="space-y-7">
      <section className="rounded-lg border border-slate-800 bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950/70 p-7 shadow-2xl shadow-black/20">
        <div className="max-w-3xl">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-sm font-medium text-blue-300">
            <ShieldCheck size={16} />
            Internal HR knowledge assistant
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-white">
            Welcome to HR Policy Copilot
          </h1>
          <p className="mt-3 text-base leading-7 text-slate-300">
            Ask employee policy questions and receive clear answers grounded in approved HR documents with citations, confidence scoring, and retrieved policy context.
          </p>
          <Link
            to="/chat"
            className="mt-6 inline-flex items-center gap-2 rounded-md bg-blue-500 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 hover:bg-blue-400"
          >
            Ask HR
            <ArrowRight size={16} />
          </Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          { label: "Preloaded documents", value: "6", icon: FileText },
          { label: "Employee uploads", value: "Disabled", icon: ShieldCheck },
          { label: "Answer mode", value: "Cited RAG", icon: MessageSquareText }
        ].map((item) => (
          <div key={item.label} className="rounded-lg border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-black/10">
            <item.icon className="text-blue-300" size={22} />
            <div className="mt-4 text-2xl font-semibold text-white">{item.value}</div>
            <div className="text-sm text-slate-400">{item.label}</div>
          </div>
        ))}
      </section>

      <section className="rounded-lg border border-slate-800 bg-slate-900 p-6 shadow-xl shadow-black/10">
        <div className="mb-4 flex items-center gap-2">
          <Clock size={19} className="text-blue-300" />
          <h2 className="text-lg font-semibold text-white">Suggested questions</h2>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          {questions.map((question) => (
            <Link
              key={question}
              to={`/chat?question=${encodeURIComponent(question)}`}
              className="rounded-md border border-slate-800 bg-slate-950/60 px-4 py-3 text-sm font-medium text-slate-300 hover:border-blue-500/50 hover:bg-blue-500/10 hover:text-blue-200"
            >
              {question}
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
