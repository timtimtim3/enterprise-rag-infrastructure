import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { chatsApi } from "../api/chats";
import type { AskRequest } from "../types/api";

export const chatKeys = {
  all: ["chats"] as const,
  list: () => [...chatKeys.all, "list"] as const,
  messages: (chatId: string) => [...chatKeys.all, chatId, "messages"] as const,
  sources: (chatId: string, messageId: string) =>
    [...chatKeys.all, chatId, "messages", messageId, "sources"] as const,
};

export function useChatList() {
  return useQuery({
    queryKey: chatKeys.list(),
    queryFn: () => chatsApi.list(),
    staleTime: 30_000,
  });
}

export function useChatMessages(chatId: string | null) {
  return useQuery({
    queryKey: chatKeys.messages(chatId ?? ""),
    queryFn: () => chatsApi.listMessages(chatId!),
    enabled: !!chatId,
    staleTime: 0,
  });
}

export function useMessageSources(
  chatId: string | null,
  messageId: string | null
) {
  return useQuery({
    queryKey: chatKeys.sources(chatId ?? "", messageId ?? ""),
    queryFn: () => chatsApi.listMessageSources(chatId!, messageId!),
    enabled: !!chatId && !!messageId,
    staleTime: Infinity,
  });
}

export function useCreateChat() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: AskRequest) => chatsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.list() });
    },
  });
}

export function useAddMessage(chatId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: AskRequest) => chatsApi.addMessage(chatId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages(chatId) });
      queryClient.invalidateQueries({ queryKey: chatKeys.list() });
    },
  });
}

export function useDeleteChat() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (chatId: string) => chatsApi.delete(chatId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.list() });
    },
  });
}
