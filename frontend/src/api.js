const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export async function apiRequest(path, { method = 'GET', token, body } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers.Authorization = `Token ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  const contentType = response.headers.get('content-type') || '';
  const data = contentType.includes('application/json') ? await response.json() : null;

  if (!response.ok) {
    const error = data?.detail || data?.non_field_errors?.[0] || 'Erreur API';
    throw new Error(error);
  }

  return data;
}

export async function login(username, password) {
  return apiRequest('/api/v1/auth/login/', {
    method: 'POST',
    body: { username, password },
  });
}

export async function getRestaurants(token) {
  return apiRequest('/api/v1/admin/restaurants/', { token });
}

export async function createRestaurant(token, payload) {
  return apiRequest('/api/v1/admin/restaurants/', {
    method: 'POST',
    token,
    body: payload,
  });
}

export async function suspendRestaurant(token, id) {
  return apiRequest(`/api/v1/admin/restaurants/${id}/suspend/`, {
    method: 'PATCH',
    token,
  });
}

export async function activateRestaurant(token, id) {
  return apiRequest(`/api/v1/admin/restaurants/${id}/activate/`, {
    method: 'PATCH',
    token,
  });
}

export async function getCategories(token) {
  return apiRequest('/api/v1/restaurant/categories/', { token });
}

export async function createCategory(token, name) {
  return apiRequest('/api/v1/restaurant/categories/', {
    method: 'POST',
    token,
    body: { name },
  });
}

export async function getOrders(token) {
  return apiRequest('/api/v1/restaurant/orders/', { token });
}

export async function createOrder(token, kind) {
  return apiRequest('/api/v1/restaurant/orders/', {
    method: 'POST',
    token,
    body: { kind },
  });
}
