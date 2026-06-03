import { api } from "./client";
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  UserInfo,
} from "../types/api";

export const authApi = {
  me: () => api.get<UserInfo>("/auth/me"),

  signIn: (data: LoginRequest) =>
    api.post<LoginResponse>("/auth/signin", data),

  signUp: (data: RegisterRequest) =>
    api.post<RegisterResponse>("/auth/signup", data),
};
