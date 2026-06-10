import { apiClient, throwApiError } from "./client";
import type {
  LoginRequest,
  RegisterRequest,
} from "../types/api";

export const authApi = {
  async me() {
    const { data, error } = await apiClient.GET("/auth/me");

    if (error) {
      throwApiError(error);
    }

    return data;
  },

  async signIn(data: LoginRequest) {
    const { data: response, error } = await apiClient.POST(
      "/auth/signin",
      {
        body: data,
      }
    );

    if (error) {
      throwApiError(error);
    }

    return response;
  },

  async signUp(data: RegisterRequest) {
    const { data: response, error } = await apiClient.POST(
      "/auth/signup",
      {
        body: data,
      }
    );

    if (error) {
      throwApiError(error);
    }
    
    return response;
  },

  async signOut() {
    const { error } = await apiClient.POST(
      "/auth/signout",
    );

    if (error) {
      throwApiError(error);
    }    
  },
};
