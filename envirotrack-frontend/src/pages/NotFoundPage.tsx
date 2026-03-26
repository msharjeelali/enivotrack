import { Link } from 'react-router-dom';

export function NotFoundPage() {
  return (
    <div className="screen-center stack-sm">
      <h2>Page Not Found</h2>
      <p>The page you are looking for does not exist.</p>
      <Link className="btn btn-primary" to="/dashboard">Go to dashboard</Link>
    </div>
  );
}
