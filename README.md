# Chartnalyze (Flask Backend)

**AI-powered market analysis meets financial education — all in one smart platform.**

---

## 🚀 Installation

### 1. Install dependencies

```sh
pip install -r requirements.txt
```

### 2. Create environment configuration

```sh
cp .env.example .env
```

### 3. Generate secret keys

Automatically generate `SECRET_KEY`, `HASH_KEY`, and `JWT_SECRET_KEY` and insert them into `.env`:

```sh
make generate-secret-key
```

### 4. Run database migrations

Use one of the following commands:

```sh
make db-upgrade         # Apply migrations
make db-downgrade       # Roll back migrations
make db-fresh           # Reset and re-apply migrations
make db-fresh-seed      # Reset, re-apply migrations, and seed data
```

---

## 👟 Running

### Run the development server

```sh
flask run --port 8000                     # Run normally
flask run --debug --port 8000            # Run in debug mode
```

### Run unit or feature tests

```sh
# Documentation for testing is coming soon...
```

---

## 🐳 Docker

### 1. Create environment configuration for Docker

```sh
cp .env.docker.example .env.docker
```

### 2. Pass your secret keys manually to the `.env.docker` file

```sh
vim .env.docker
```

### 3. Build and run with Docker

```sh
docker compose up --build -d
```

Once started, the app will be accessible at:

```
http://localhost:80
```

### Seed database in Docker

```sh
docker compose exec chartnalyze-flask bash -c "make db-fresh-seed"
```

---

## 📡 Routes

API routes are documented in the `postman_collection.json` file.

Preview the contents:

```sh
head postman_collection.json
```

---

## 📄 License

This project is open-source under the **MIT License**.

Made with ❤️ by **Chartnalyze**
