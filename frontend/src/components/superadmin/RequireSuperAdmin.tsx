import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

export function RequireSuperAdmin() {
  const isSuperAdmin = localStorage.getItem('vox-ai-superadmin') === 'true';
  return isSuperAdmin ? <Outlet /> : <Navigate to="/superadmin/login" replace />;
}
