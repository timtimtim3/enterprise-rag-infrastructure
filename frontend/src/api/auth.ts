import { api } from "./client";
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
} from "../types/api";

export const authApi = {
  signIn: (data: LoginRequest) =>
    api.post<LoginResponse>("/auth/signin", data),

  signUp: (data: RegisterRequest) =>
    api.post<RegisterResponse>("/auth/singup", data),
};
