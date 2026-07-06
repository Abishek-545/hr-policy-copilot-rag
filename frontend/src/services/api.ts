import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000
});

export type Source = {
  document: string;
  page: number;
  snippet: string;
  score: number;
};

export type RetrievedContext = {
  document: string;
  page: number;
  category: string;
  text: string;
  score: number;
};

export type ChatResponse = {
  answer: string;
  confidence: number;
  sources: Source[];
  retrieved_context: RetrievedContext[];
  response_time?: number;
};

export type PolicyDocument = {
  name: string;
  title: string;
  category: string;
  pages: number;
  chunks: number;
  last_indexed: string;
  description: string;
  size_kb: number;
};

export type Analytics = {
  documents_count: number;
  chunks_count: number;
  questions_asked: number;
  average_response_time: number;
  most_referenced_documents: { document: string; count: number }[];
  common_question_categories: { category: string; count: number }[];
};

export async function askHr(question: string) {
  const { data } = await api.post<ChatResponse>("/chat", { question });
  return data;
}

export async function getDocuments() {
  const { data } = await api.get<{ documents: PolicyDocument[] }>("/documents");
  return data.documents;
}

export async function getAnalytics() {
  const { data } = await api.get<Analytics>("/analytics");
  return data;
}
