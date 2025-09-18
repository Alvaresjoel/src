import { Navigate, redirect } from 'react-router-dom';
import { getAuthToken } from '../utils/auth';

export default function RequireAuth() {
    const token = getAuthToken();
    if (!token) {
        redirect('/login');
    }
};
