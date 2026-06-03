export interface AskRequest {
  query: string;
}

export interface Usage {
  completion_tokens: number;
  prompt_tokens: number;
  total_tokens: number;
}

export interface Source {
  doc_id: string;
  source_index: number;
  title: string;
  source_path: string;
  source_type: string;
  doc_type: string;
  chunk_indices: number[];
}

export interface AskResponse {
  chat_id: string;
  query_message_id: string;
  answer_message_id: string;
  answer: string;
  model: string | null;
  finish_reason: string | null;
  usage: Usage;
  sources: Source[];
}

export interface ChatInfo {
  chat_id: string;
  title: string | null;
}

export type MessageRole = "user" | "assistant" | "system";

export interface MessageInfo {
  message_id: string;
  role: MessageRole;
  content: string;
}

export interface MessageSourceInfo {
  doc_id: string;
  source_index: number;
  chunk_indices: number[];
  title: string;
  source_path: string;
  source_type: string;
  doc_type: string;
  score?: number | null;
  reranker_score?: number | null;
}

export interface ListChatsResponse {
  chats: ChatInfo[];
}

export interface ListMessagesResponse {
  messages: MessageInfo[];
}

export interface ListMessageSourcesResponse {
  message_sources: MessageSourceInfo[];
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface RegisterResponse {
  user_id: string;
  username: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  user_id: string;
  username: string;
}

export interface UserInfo {
  user_id: string;
  username: string;
}

export interface ApiError {
  detail: string | { loc: (string | number)[]; msg: string; type: string }[];
}
