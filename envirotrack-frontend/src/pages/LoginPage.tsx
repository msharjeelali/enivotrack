import { Activity, AlertCircle, RefreshCw, User, KeyRound } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError('');
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to log in.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-screen">
      <div className="login-card">
        <div className="login-brand">
          <span><Activity size={28} /></span>
          <h1>EnviroTrack</h1>
          <p>Access the admin dashboard securely</p>
        </div>
        {error ? <div className="login-error"><AlertCircle size={16} /> {error}</div> : null}
        <label>
          Username
          <div className="input-wrap"><User size={16} /><input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="admin" /></div>
        </label>
        <label>
          Password
          <div className="input-wrap"><KeyRound size={16} /><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="admin123" /></div>
        </label>
        <button className="btn btn-primary" onClick={handleSubmit} disabled={loading || !username || !password}>
          {loading ? <><RefreshCw size={16} className="spin" /> Verifying…</> : 'Log In'}
        </button>
        <small>Demo credentials: admin / admin123</small>
      </div>
    </div>
  );
}
