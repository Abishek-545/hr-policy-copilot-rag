import { useEffect, useState } from "react";
import { FileText } from "lucide-react";
import { getDocuments, PolicyDocument } from "../services/api";

export default function Documents() {
  const [documents, setDocuments] = useState<PolicyDocument[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDocuments().then(setDocuments).finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold text-white">Policy Documents</h1>
        <p className="mt-1 text-sm text-slate-400">
          View-only library of HR documents indexed by the assistant.
        </p>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        {loading && <div className="text-sm text-slate-400">Loading policy documents...</div>}
        {documents.map((document) => (
          <article key={document.name} className="rounded-lg border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-black/10">
            <div className="flex items-start gap-4">
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-blue-500/30 bg-blue-500/10 text-blue-300">
                <FileText size={21} />
              </div>
              <div className="min-w-0 flex-1">
                <h2 className="text-base font-semibold text-white">{document.title}</h2>
                <div className="mt-1 text-sm text-blue-300">{document.category}</div>
                <p className="mt-3 text-sm leading-6 text-slate-400">{document.description}</p>
                <div className="mt-4 grid grid-cols-2 gap-3 text-sm md:grid-cols-4">
                  <Metric label="Pages" value={document.pages.toString()} />
                  <Metric label="Chunks" value={document.chunks.toString()} />
                  <Metric label="Size" value={`${document.size_kb} KB`} />
                  <Metric label="Indexed" value={document.last_indexed ? "Yes" : "Pending"} />
                </div>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-slate-800 bg-slate-950/70 px-3 py-2">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-1 font-semibold text-slate-100">{value}</div>
    </div>
  );
}
