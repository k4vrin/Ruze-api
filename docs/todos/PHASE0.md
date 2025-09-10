## Phase 0 — Repo & Tooling (Scaffolding)

This phase sets up the foundation of the Ruze backend project. The goal is to make sure the repo has all the essential configs, tools, and checks before writing actual app logic.

- [x] **Create repo `ruze-api` with LICENSE, README**  
  Start a new GitHub repo with a clear license (e.g., BSL for commercial) and a README that explains the project.

- [x] **Add `.editorconfig`, `.gitignore` (Python, FastAPI, Alembic, Docker)**  
  `.editorconfig` enforces consistent code style (indentation, spaces, line endings).  
  `.gitignore` ensures you don’t commit unnecessary files (e.g., venv, `__pycache__`, build artifacts, Docker volumes).

- [x] **Add `docker-compose.yml` (Postgres + Redis + Adminer/pgweb optional)**  
  Define local development services:
    - Postgres for database
    - Redis for caching / background tasks
    - Adminer or pgweb for simple DB management in the browser

- [x] **Set up `uv` or `poetry` and lock dependencies**  
  Pick a dependency manager (`uv` is modern and fast, `poetry` is popular).  
  Use it to install FastAPI, Uvicorn, and other core libraries, then lock exact versions in a lock file.

- [x] **Add `pyproject.toml` with ruff, black, mypy configs**  
  Centralize tool configs in `pyproject.toml`:
    - **ruff** for linting (fast, replaces flake8/isort)
    - **black** for auto-formatting
    - **mypy** for static typing checks

- [x] **Configure `pre-commit` hooks (ruff/black/mypy/flake8 end-of-file-fixer)**  
  Set up Git hooks so that before every commit, code style and typing checks run automatically.  
  This helps catch mistakes early and keeps the repo clean.

---
## Phase 1 — Configuration & Database
- [ ] Create `app/core/settings.py` with `pydantic-settings`
    - [ ] Variables: `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, `ACCESS_TTL_MIN`, `REFRESH_TTL_DAYS`, `CORS_ORIGINS`, `ENV`, `OPENROUTER_KEY`
    - [ ] Provide `.env.example` (see Appendix A)
- [ ] DB bootstrapping
    - [ ] `app/db/session.py` (engine, sessionmaker, async if chosen)
    - [ ] `app/db/base.py` (Declarative `Base`)
    - [ ] Alembic init + env config (async or sync)
- [ ] **Models (initial)**
    - [ ] `User` (id, email UNIQUE, password_hash, is_active, is_admin, created_at)
    - [ ] `RefreshToken` (id, user_id, jti, expires_at, revoked)
- [ ] **Migration**: `alembic revision --autogenerate -m "init"`; upgrade head
- [ ] **DoD**: DB connects, tables exist, settings load from `.env`
