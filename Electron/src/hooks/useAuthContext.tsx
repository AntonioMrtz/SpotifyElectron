import {
  createContext,
  useContext,
  useState,
  useEffect,
  useMemo,
  ReactNode,
} from 'react';
import { getTokenUsername } from 'utils/token';
import { TOKEN_KEY, ROLE_KEY } from '../constants/auth';

type AuthContextType = {
  username: string | null;
  token: string | null;
  role: string | null;
  setAuthData: (username: string, token: string, role: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [username, setUsername] = useState<string | null>(getTokenUsername());
  const [token, setToken] = useState<string | null>(
    localStorage.getItem(TOKEN_KEY),
  );
  const [role, setRole] = useState<string | null>(
    localStorage.getItem(ROLE_KEY),
  );
  // Global authentication context provider
  useEffect(() => {
    setUsername(getTokenUsername());
  }, [token]);

  const setAuthData = (
    newUsername: string,
    newToken: string,
    newRole: string,
  ) => {
    setUsername(newUsername);
    setToken(newToken);
    setRole(newRole);

    localStorage.setItem(TOKEN_KEY, newToken);
    localStorage.setItem(ROLE_KEY, newRole);
  };

  const logout = () => {
    setUsername(null);
    setToken(null);
    setRole(null);

    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(ROLE_KEY);
  };

  const value = useMemo(
    () => ({
      username,
      token,
      role,
      setAuthData,
      logout,
    }),
    [username, token, role],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within AuthProvider');
  }
  return context;
}
