import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { getTokenUsername } from 'utils/token';

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
    localStorage.getItem('token')
  );
  const [role, setRole] = useState<string | null>(
    localStorage.getItem('role')
  );
  // Global authentication context provider
  useEffect(() => {

    setUsername(getTokenUsername());
  
  }, [token]);

  const setAuthData = (username: string, token: string, role: string) => {
    setUsername(username);
    setToken(token);
    setRole(role);

    localStorage.setItem('token', token);
    localStorage.setItem('role', role);
  };

  const logout = () => {
    setUsername(null);
    setToken(null);
    setRole(null);

    localStorage.removeItem('token');
    localStorage.removeItem('role');
  };

  return (
    <AuthContext.Provider value={{ username, token, role, setAuthData, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within AuthProvider');
  }
  return context;
}