import { mockAuthUser } from '@/services/mocks/data';
import type { AuthUser } from '@/types';

const TOKEN_KEY = 'envirotrack_token';

export const authService = {
  async login(username: string, password: string): Promise<AuthUser> {
    await new Promise((resolve) => setTimeout(resolve, 700));
    if (username === 'admin' && password === 'admin123') {
      localStorage.setItem(TOKEN_KEY, 'demo-token');
      localStorage.setItem('envirotrack_user', JSON.stringify(mockAuthUser));
      return mockAuthUser;
    }
    throw new Error('Incorrect username or password.');
  },
  logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem('envirotrack_user');
  },
  getStoredUser(): AuthUser | null {
    const raw = localStorage.getItem('envirotrack_user');
    return raw ? (JSON.parse(raw) as AuthUser) : null;
  },
};
