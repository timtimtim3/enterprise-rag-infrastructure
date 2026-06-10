import {
  createContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { authApi } from "../api/auth";
import type { LoginResponse } from "../types/api";
import { useQueryClient } from "@tanstack/react-query";

interface AuthUser {
  user_id: string;
  username: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  login: (response: LoginResponse) => void;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const queryClient = useQueryClient();

  useEffect(() => {
    authApi
      .me()
      .then((info) => setUser({ user_id: info.user_id, username: info.username }))
      .catch(() => setUser(null))
      .finally(() => setIsLoading(false));
  }, []);

  const login = useCallback((response: LoginResponse) => {
    setUser({ user_id: response.user_id, username: response.username });
  }, []);

  const logout = useCallback(async () => {
    try {
      await authApi.signOut();
    } catch {
      // ignore
    } finally {
      queryClient.clear();
      setUser(null);
    }
  }, [queryClient]);

  return (
    <AuthContext.Provider
      value={{ user, login, logout, isAuthenticated: user !== null, isLoading }}
    >
      {children}
    </AuthContext.Provider>
  );
}
