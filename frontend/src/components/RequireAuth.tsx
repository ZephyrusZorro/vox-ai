import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

/**
 * Wraps protected routes.
 * Checks localStorage for 'vox-ai-authed' === 'true'.
 * Redirects to /login with ?from= if not authenticated.
 */
export function RequireAuth({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const isAuthed = localStorage.getItem('vox-ai-authed') === 'true';

  if (!isAuthed) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}

export function isAuthenticated(): boolean {
  return localStorage.getItem('vox-ai-authed') === 'true';
}

export function signOut(): void {
  localStorage.removeItem('vox-ai-authed');
  localStorage.removeItem('vox-ai-superadmin');
  localStorage.removeItem('vox-ai-tenant-id');
  localStorage.removeItem('vox-ai-email');
  localStorage.removeItem('vox-ai-clinic-name');
}
