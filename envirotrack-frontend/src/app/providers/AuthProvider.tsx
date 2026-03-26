import { useEffect, useMemo, useState } from 'react';
import { AuthContext } from '@/context/AuthContext';
import { authService } from '@/services/api/authService';
import type { AuthUser } from '@/types';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setUser(authService.getStoredUser());
    setLoading(false);
  }, []);

  const value = useMemo(() => ({
    user,
    loading,
    login: async (username: string, password: string) => {
      const nextUser = await authService.login(username, password);
      setUser(nextUser);
    },
    logout: () => {
      authService.logout();
      setUser(null);
    },
  }), [user, loading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
