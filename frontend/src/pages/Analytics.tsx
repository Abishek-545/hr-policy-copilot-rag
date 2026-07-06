import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { BarChart3, FileText, Gauge, MessageSquare, Timer } from "lucide-react";
import { Analytics as AnalyticsType, getAnalytics } from "../services/api";

const emptyAnalytics: AnalyticsType = {
  documents_count: 0,
  chunks_count: 0,
  questions_asked: 0,
  average_response_time: 0,
  most_referenced_documents: [],
  common_question_categories: []
};

export default function Analytics() {
  const [analytics, setAnalytics] = useState<AnalyticsType>(emptyAnalytics);

  useEffect(() => {
    getAnalytics().then(setAnalytics);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-white">Analytics</h1>
        <p className="mt-1 text-sm text-slate-400">Simple operational metrics for the HR assistant.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Stat label="Policy documents" value={analytics.documents_count} icon={FileText} />
        <Stat label="Chunks indexed" value={analytics.chunks_count} icon={Gauge} />
        <Stat label="Questions asked" value={analytics.questions_asked} icon={MessageSquare} />
        <Stat label="Avg response time" value={`${analytics.average_response_time}s`} icon={Timer} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Panel title="Most referenced documents">
          {analytics.most_referenced_documents.length === 0 ? (
            <EmptyState />
          ) : (
            analytics.most_referenced_documents.map((item) => (
              <Row key={item.document} label={item.document} value={item.count} />
            ))
          )}
        </Panel>
        <Panel title="Common question categories">
          {analytics.common_question_categories.length === 0 ? (
            <EmptyState />
          ) : (
            analytics.common_question_categories.map((item) => (
              <Row key={item.category} label={item.category} value={item.count} />
            ))
          )}
        </Panel>
      </div>
    </div>
  );
}

function Stat({ label, value, icon: Icon }: { label: string; value: string | number; icon: typeof BarChart3 }) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-black/10">
      <Icon className="text-blue-300" size={21} />
      <div className="mt-4 text-2xl font-semibold text-white">{value}</div>
      <div className="text-sm text-slate-400">{label}</div>
    </div>
  );
}

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="rounded-lg border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-black/10">
      <h2 className="text-base font-semibold text-white">{title}</h2>
      <div className="mt-4 space-y-3">{children}</div>
    </section>
  );
}

function Row({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex items-center justify-between rounded-md border border-slate-800 bg-slate-950/70 px-3 py-2 text-sm">
      <span className="font-medium text-slate-300">{label}</span>
      <span className="rounded-full border border-blue-500/30 bg-blue-500/10 px-2 py-0.5 text-xs font-semibold text-blue-300">{value}</span>
    </div>
  );
}

function EmptyState() {
  return <div className="rounded-md border border-slate-800 bg-slate-950/70 p-4 text-sm text-slate-400">No questions have been asked yet.</div>;
}
