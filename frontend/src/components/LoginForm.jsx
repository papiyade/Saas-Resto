import { useState } from 'react';

export default function LoginForm({ onLogin, loading }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const submit = (e) => {
    e.preventDefault();
    onLogin(username, password);
  };

  return (
    <form className="card" onSubmit={submit}>
      <h2>Connexion</h2>
      <input
        placeholder="Nom utilisateur"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Mot de passe"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button disabled={loading}>{loading ? 'Connexion...' : 'Se connecter'}</button>
    </form>
  );
}
