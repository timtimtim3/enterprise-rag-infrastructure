import {
  createContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { authApi } from "../api/auth";
import type { LoginJWTResponse } from "../types/api";
import { useQueryClient } from "@tanstack/react-query";
import { initializeAuth, setAccessToken } from "../api/client";

interface AuthUser {
  user_id: string;
  username: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  login: (response: LoginJWTResponse) => void;
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
    async function bootstrapAuth() {
      try {
        const restored = await initializeAuth();

        if (!restored) {
          setUser(null);
          return;
        }

        const info = await authApi.meJwt();
        setUser({
          user_id: info.user_id,
          username: info.username,
        });
      } catch {
        setAccessToken(null);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    }

    bootstrapAuth();
  }, []); 

  const login = useCallback((response: LoginJWTResponse) => {
    setAccessToken(response.access_token);
    setUser({ user_id: response.user_id, username: response.username });
  }, []);

  const logout = useCallback(async () => {
    try {
      await authApi.signOutJwt();
    } catch {
      // ignore
    } finally {
      setAccessToken(null);
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
