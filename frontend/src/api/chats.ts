import { api } from "./client";
import type {
  AskRequest,
  AskResponse,
  ListChatsResponse,
  ListMessageSourcesResponse,
  ListMessagesResponse,
} from "../types/api";

export const chatsApi = {
  list: () => api.get<ListChatsResponse>("/chats"),

  create: (data: AskRequest) => api.post<AskResponse>("/chats", data),

  delete: (chatId: string) => api.delete(`/chats/${chatId}`),

  listMessages: (chatId: string) =>
    api.get<ListMessagesResponse>(`/chats/${chatId}/messages`),

  addMessage: (chatId: string, data: AskRequest) =>
    api.post<AskResponse>(`/chats/${chatId}/messages`, data),

  listMessageSources: (chatId: string, messageId: string) =>
    api.get<ListMessageSourcesResponse>(
      `/chats/${chatId}/messages/${messageId}/sources`
    ),
};
