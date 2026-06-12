import { authGet, authPost, authDelete, throwApiError } from "./client";
import type {
  AskRequest,
} from "../types/api";

export const chatsApi = {
  async list() {
    const { data, error } = await authGet("/chats");

    if (error) {
      throwApiError(error);
    }

    return data;
  },

  async create(data: AskRequest) {
    const { data: response, error } = await authPost(
      "/chats",
      {
        body: data,
      }
    );

    if (error) {
      throwApiError(error);
    }

    return response;
  },

  async delete(chatId: string) {
    const { error } = await authDelete(
      "/chats/{chat_id}",
      {
        params: {
          path: {
            chat_id: chatId,
          },
        },
      }
    );

    if (error) {
      throwApiError(error);
    }
  },

  async listMessages(chatId: string) {
    const { data, error } = await authGet(
      "/chats/{chat_id}/messages",
      {
        params: {
          path: {
            chat_id: chatId,
          },
        },
      }
    );

    if (error) {
      throwApiError(error);
    }
    
    return data;
  },

  async addMessage(chatId: string, data: AskRequest) {
    const { data: response, error } = await authPost(
      "/chats/{chat_id}/messages",
      {
        params: {
          path: {
            chat_id: chatId,
          },
        },
        body: data,
      }
    );

    if (error) {
      throwApiError(error);
    }

    return response;
  },

  async listMessageSources(chatId: string, messageId: string) {
    const { data, error } = await authGet(
      "/chats/{chat_id}/messages/{message_id}/sources",
      {
        params: {
          path: {
            chat_id: chatId,
            message_id: messageId,
          },
        },
      }
    );

    if (error) {
      throwApiError(error);
    }

    return data;
  },
};
