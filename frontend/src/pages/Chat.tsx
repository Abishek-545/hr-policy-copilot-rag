import { FormEvent, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { AlertCircle, Bot, ChevronDown, Send, User } from "lucide-react";
import { askHr, ChatResponse } from "../services/api";

type Message = {
  role: "user" | "assistant";
  content: string;
  response?: ChatResponse;
};

export default function Chat() {
  const [searchParams] = useSearchParams();
  const initialQuestion = searchParams.get("question") || "";
  const [question, setQuestion] = useState(initialQuestion);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setQuestion(initialQuestion);
  }, [initialQuestion]);

  async function submit(event?: FormEvent) {
    event?.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    setMessages((current) => [...current, { role: "user", content: trimmed }]);
    setQuestion("");
    setLoading(true);
    setError("");

    try {
      const response = await askHr(trimmed);
      setMessages((current) => [
        ...current,
        { role: "assistant", content: response.answer, response }
      ]);
    } catch {
      setError("The HR assistant could not be reached. Please check that the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_360px]">
      <section className="rounded-lg border border-slate-800 bg-slate-900 shadow-2xl shadow-black/20">
        <div className="border-b border-slate-800 px-5 py-4">
          <h1 className="text-xl font-semibold text-white">Ask HR</h1>
          <p className="mt-1 text-sm text-slate-400">
            Answers are restricted to the indexed HR policy library.
          </p>
        </div>

        <div className="h-[560px] space-y-5 overflow-y-auto px-5 py-5">
          {messages.length === 0 && (
            <div className="rounded-lg border border-dashed border-slate-700 bg-slate-950/70 p-8 text-center">
              <Bot className="mx-auto text-blue-300" size={34} />
              <h2 className="mt-3 text-base font-semibold text-white">How can HR help?</h2>
              <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-400">
                Ask about leave, remote work, expenses, conduct, security, onboarding, or other available policies.
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index} className={`flex gap-3 ${message.role === "user" ? "justify-end" : ""}`}>
              {message.role === "assistant" && (
                <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-blue-500 text-white">
                  <Bot size={17} />
                </div>
              )}
              <div className={`max-w-3xl rounded-lg px-4 py-3 ${message.role === "user" ? "bg-blue-500 text-white shadow-lg shadow-blue-500/20" : "border border-slate-800 bg-slate-950 text-slate-200"}`}>
                <div className="whitespace-pre-wrap text-sm leading-6">{message.content}</div>
                {message.response && (
                  <div className="mt-4 space-y-3">
                    <div className="flex flex-wrap gap-2 text-xs">
                      <span className="rounded-full border border-slate-700 bg-slate-900 px-2.5 py-1 font-medium text-slate-300">
                        Confidence {(message.response.confidence * 100).toFixed(0)}%
                      </span>
                      {message.response.response_time !== undefined && (
                        <span className="rounded-full border border-slate-700 bg-slate-900 px-2.5 py-1 font-medium text-slate-300">
                          {message.response.response_time}s
                        </span>
                      )}
                    </div>
                    <div className="rounded-md border border-slate-800 bg-slate-900 p-3">
                      <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">Sources</div>
                      <div className="space-y-2">
                        {message.response.sources.map((source, sourceIndex) => (
                          <div key={`${source.document}-${sourceIndex}`} className="text-xs leading-5 text-slate-300">
                            <span className="font-semibold text-white">{source.document}</span>, page {source.page}
                          </div>
                        ))}
                      </div>
                    </div>
                    <details className="rounded-md border border-slate-800 bg-slate-900 p-3 text-xs text-slate-300">
                      <summary className="flex cursor-pointer items-center gap-2 font-semibold text-white">
                        <ChevronDown size={14} />
                        Retrieved context
                      </summary>
                      <div className="mt-3 space-y-3">
                        {message.response.retrieved_context.map((context, contextIndex) => (
                          <div key={contextIndex} className="border-t border-slate-800 pt-3">
                            <div className="font-semibold text-slate-100">
                              {context.document}, page {context.page} - score {context.score}
                            </div>
                            <p className="mt-1 leading-5 text-slate-400">{context.text}</p>
                          </div>
                        ))}
                      </div>
                    </details>
                  </div>
                )}
              </div>
              {message.role === "user" && (
                <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-slate-700 text-white">
                  <User size={17} />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-3 text-sm text-slate-400">
              <div className="h-2 w-2 animate-pulse rounded-full bg-blue-400" />
              Retrieving policies and drafting a grounded answer...
            </div>
          )}
        </div>

        {error && (
          <div className="mx-5 mb-4 flex items-center gap-2 rounded-md border border-red-500/30 bg-red-950/60 px-3 py-2 text-sm text-red-200">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        <form onSubmit={submit} className="border-t border-slate-800 p-4">
          <div className="flex gap-3">
            <input
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask an HR policy question..."
              className="min-w-0 flex-1 rounded-md border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-blue-400 focus:ring-2 focus:ring-blue-500/20"
            />
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center gap-2 rounded-md bg-blue-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Send size={16} />
              Send
            </button>
          </div>
        </form>
      </section>

      <aside className="rounded-lg border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-black/10">
        <h2 className="text-base font-semibold text-white">Answer policy</h2>
        <div className="mt-4 space-y-3 text-sm leading-6 text-slate-400">
          <p>No employee document uploads are available.</p>
          <p>Answers cite the preloaded policy PDFs only.</p>
          <p>If the answer is not found, the assistant directs the employee to HR.</p>
        </div>
      </aside>
    </div>
  );
}
