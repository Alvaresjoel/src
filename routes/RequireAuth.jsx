import { Navigate, useLocation } from 'react-router-dom';
import { getAuthToken } from '../utils/auth';

export default function RequireAuth({ children }) {
  const isAuthed = !!getAuthToken();
  const location = useLocation();
  if (!isAuthed) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
}


