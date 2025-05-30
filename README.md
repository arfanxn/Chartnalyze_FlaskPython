# Chartnalyze (Flask Backend)

**AI-powered market analysis meets financial education — all in one platform.**

---

## 🚀 Getting Started

### 📍 Local Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

3. **Generate secret keys**
   Automatically generate `SECRET_KEY`, `HASH_KEY`, and `JWT_SECRET_KEY`:
   ```bash
   make generate-secret-key
   ```

4. **Run database migrations**
   Choose one:
   ```bash
   make db-upgrade         # Apply migrations
   make db-downgrade       # Roll back migrations
   make db-fresh           # Reset and re-apply migrations
   make db-fresh-seed      # Reset, re-apply, and seed data
   ```

5. **Start the development server**
   ```bash
   flask run --port 8000              # Standard mode
   flask run --debug --port 8000      # Debug mode
   ```

6. **Run tests**
   *(Coming soon: test documentation)*

---

### 🐳 Docker Installation

1. **Set up Docker environment**
   ```bash
   cp .env.example .docker.env
   ```

2. **Generate secret keys**
   ```bash
   make generate-secret-key
   ```

3. **Build and start the app**
   ```bash
   docker compose up --build -d
   ```

   App will be available at:
   ```
   http://localhost:80
   ```

4. **Run migrations and seed the database in Docker** (Run if needed)
   ```bash
   docker compose exec chartnalyze_flask make db-fresh-seed
   ```

---

## 📡 API Routes

API endpoints are documented in `postman_collection.json`.

Preview the file:
```bash
head postman_collection.json
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

Made with ❤️ by **Chartnalyze** 

---

## 👥 Contributors

A huge thanks to the amazing people who have contributed to this project! 🚀

| [![Arfanxn](https://avatars.githubusercontent.com/u/82434988?v=4&)](https://github.com/arfanxn) | [![Deny Faishal Ardiyanto](https://avatars.githubusercontent.com/u/122851646?v=4)](https://github.com/1lwlawck) |
|:--:|:--:|
| [**Arfanxn**](https://github.com/arfanxn) | [**Deny Faishal Ardiyanto**](https://github.com/1lwlawck) |

Want to contribute? [Join us on GitHub!](https://github.com/your-username/chartnalyze/graphs/contributors)
