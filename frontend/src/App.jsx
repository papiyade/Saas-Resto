import { useEffect, useState } from 'react';
import LoginForm from './components/LoginForm';
import {
  activateRestaurant,
  createCategory,
  createOrder,
  createRestaurant,
  getCategories,
  getOrders,
  getRestaurants,
  login,
  suspendRestaurant,
} from './api';

export default function App() {
  const [session, setSession] = useState(() => {
    const raw = localStorage.getItem('session');
    return raw ? JSON.parse(raw) : null;
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const [restaurants, setRestaurants] = useState([]);
  const [categories, setCategories] = useState([]);
  const [orders, setOrders] = useState([]);
  const [newRestaurant, setNewRestaurant] = useState({ name: '', slug: '' });
  const [newCategory, setNewCategory] = useState('');

  const token = session?.token;
  const isPlatformAdmin = session?.user?.is_platform_admin;

  useEffect(() => {
    if (!token) return;
    const load = async () => {
      try {
        if (isPlatformAdmin) {
          const list = await getRestaurants(token);
          setRestaurants(list);
        } else {
          const [catList, orderList] = await Promise.all([getCategories(token), getOrders(token)]);
          setCategories(catList);
          setOrders(orderList);
        }
      } catch (e) {
        setError(e.message);
      }
    };
    load();
  }, [token, isPlatformAdmin]);

  const handleLogin = async (username, password) => {
    setLoading(true);
    setError('');
    try {
      const data = await login(username, password);
      setSession(data);
      localStorage.setItem('session', JSON.stringify(data));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('session');
    setSession(null);
    setRestaurants([]);
    setCategories([]);
    setOrders([]);
  };

  const submitRestaurant = async (e) => {
    e.preventDefault();
    try {
      await createRestaurant(token, newRestaurant);
      setNewRestaurant({ name: '', slug: '' });
      setRestaurants(await getRestaurants(token));
    } catch (e) {
      setError(e.message);
    }
  };

  const toggleRestaurant = async (restaurant) => {
    try {
      if (restaurant.is_active) {
        await suspendRestaurant(token, restaurant.id);
      } else {
        await activateRestaurant(token, restaurant.id);
      }
      setRestaurants(await getRestaurants(token));
    } catch (e) {
      setError(e.message);
    }
  };

  const submitCategory = async (e) => {
    e.preventDefault();
    try {
      await createCategory(token, newCategory);
      setNewCategory('');
      setCategories(await getCategories(token));
    } catch (e) {
      setError(e.message);
    }
  };

  const submitOrder = async (kind) => {
    try {
      await createOrder(token, kind);
      setOrders(await getOrders(token));
    } catch (e) {
      setError(e.message);
    }
  };

  if (!session) {
    return (
      <main className="container">
        <h1>SaaS Resto</h1>
        <p>Frontend connecté au backend Django (Token Auth).</p>
        {error && <p className="error">{error}</p>}
        <LoginForm onLogin={handleLogin} loading={loading} />
      </main>
    );
  }

  return (
    <main className="container">
      <header className="topbar">
        <h1>SaaS Resto Dashboard</h1>
        <div>
          <span>{session.user.username}</span>
          <button onClick={logout}>Déconnexion</button>
        </div>
      </header>

      {error && <p className="error">{error}</p>}

      {isPlatformAdmin ? (
        <section className="card">
          <h2>Superadmin - Restaurants</h2>
          <form onSubmit={submitRestaurant} className="row">
            <input
              placeholder="Nom restaurant"
              value={newRestaurant.name}
              onChange={(e) => setNewRestaurant((prev) => ({ ...prev, name: e.target.value }))}
              required
            />
            <input
              placeholder="Slug"
              value={newRestaurant.slug}
              onChange={(e) => setNewRestaurant((prev) => ({ ...prev, slug: e.target.value }))}
              required
            />
            <button>Créer</button>
          </form>

          <ul>
            {restaurants.map((r) => (
              <li key={r.id} className="row between">
                <span>
                  {r.name} ({r.slug}) - {r.status}
                </span>
                <button onClick={() => toggleRestaurant(r)}>
                  {r.is_active ? 'Suspendre' : 'Activer'}
                </button>
              </li>
            ))}
          </ul>
        </section>
      ) : (
        <>
          <section className="card">
            <h2>Catégories</h2>
            <form onSubmit={submitCategory} className="row">
              <input
                placeholder="Nom catégorie"
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
                required
              />
              <button>Ajouter</button>
            </form>
            <ul>{categories.map((c) => <li key={c.id}>{c.name}</li>)}</ul>
          </section>

          <section className="card">
            <h2>Commandes</h2>
            <div className="row">
              <button onClick={() => submitOrder('dine_in')}>Nouvelle sur place</button>
              <button onClick={() => submitOrder('takeaway')}>Nouvelle à emporter</button>
              <button onClick={() => submitOrder('delivery')}>Nouvelle livraison</button>
            </div>
            <ul>
              {orders.map((o) => (
                <li key={o.id}>Commande #{o.id} - {o.kind} - {o.status}</li>
              ))}
            </ul>
          </section>
        </>
      )}
    </main>
  );
}
