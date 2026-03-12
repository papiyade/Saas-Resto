# SaaS Resto - Full Stack (Backend + Frontend)

Monorepo complet dans **un seul dossier** :
- `backend` Django + DRF + MySQL (multi-tenant par restaurant)
- `frontend` React + Vite connecté à l'API

## 1) Fonctionnalités livrées

### Back-end
- Superadmin plateforme : créer/lister/activer/suspendre des restaurants.
- Auth API par token (`/api/v1/auth/login/`).
- Isolation multi-tenant logique par `restaurant_id`.
- Endpoints restaurant : catégories, menu-items, commandes.
- Blocage automatique des comptes restaurant si restaurant suspendu (HTTP 423).

### Front-end
- Écran de connexion.
- Dashboard **superadmin** : gestion des restaurants + bouton activer/suspendre.
- Dashboard **restaurant** : gestion catégories + création commandes.
- Connexion réelle à l'API Django via token.

---

## 2) Structure

- `apps/` : apps Django (`accounts`, `restaurants`, `orders`, `common`)
- `saas_resto/` : config projet Django
- `frontend/` : app React Vite

---

## 3) Récupérer le projet

```bash
git clone <URL_DU_REPO>
cd Saas-Resto
```

---

## 4) Lancer le backend

### 4.1 Préparer l'environnement Python
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4.2 Configurer les variables
```bash
cp .env.example .env
```

### 4.3 Base de données
Par défaut : **MySQL** (recommandé prod).

Variables utilisées :
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`

Option locale rapide (sans MySQL) :
```bash
export USE_SQLITE=true
```

### 4.4 Migrations + superuser + run
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

API disponible sur `http://127.0.0.1:8000`.

---

## 5) Lancer le frontend

Dans un 2e terminal :

```bash
cd frontend
cp .env.example .env
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Front disponible sur `http://127.0.0.1:5173`.

---

## 6) Créer des utilisateurs de test (runner rapide)

### 6.1 Créer un superadmin API
```bash
python manage.py shell -c "from apps.accounts.models import User; User.objects.filter(username='platform').delete(); User.objects.create_user(username='platform',password='platform123',is_platform_admin=True,is_staff=True,is_superuser=True)"
```

### 6.2 Créer un restaurant + user restaurant
```bash
python manage.py shell -c "from apps.restaurants.models import Restaurant; from apps.accounts.models import User; r,_=Restaurant.objects.get_or_create(slug='demo-resto',defaults={'name':'Demo Resto'}); User.objects.filter(username='manager').delete(); User.objects.create_user(username='manager',password='manager123',restaurant=r)"
```

Connectez-vous dans le front avec :
- Superadmin: `platform / platform123`
- Restaurant: `manager / manager123`

---

## 7) Commandes runner (copier-coller)

### Terminal A (backend)
```bash
cd Saas-Resto
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export USE_SQLITE=true
python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "from apps.accounts.models import User; User.objects.filter(username='platform').delete(); User.objects.create_user(username='platform',password='platform123',is_platform_admin=True,is_staff=True,is_superuser=True)"
python manage.py shell -c "from apps.restaurants.models import Restaurant; from apps.accounts.models import User; r,_=Restaurant.objects.get_or_create(slug='demo-resto',defaults={'name':'Demo Resto'}); User.objects.filter(username='manager').delete(); User.objects.create_user(username='manager',password='manager123',restaurant=r)"
python manage.py runserver 0.0.0.0:8000
```

### Terminal B (frontend)
```bash
cd Saas-Resto/frontend
cp .env.example .env
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

