

### Local dev services (Docker Compose)

Prereq: Docker Desktop installed. Copy env defaults and start services:

```bash
cp -n .env.example .env 2>/dev/null || cp .env.example .env

# Start core services
docker compose up -d postgres redis

# Or include DB web UI (pgweb) via profile
docker compose --profile tools up -d
```

- Postgres: localhost:${POSTGRES_PORT:-5432} (default 5432)
- Redis: localhost:${REDIS_PORT:-6379} (default 6379)
- pgweb (optional): http://localhost:${PGWEB_PORT:-8081}

Connection strings:
- PostgreSQL: `postgresql://${POSTGRES_USER:-ruze}:${POSTGRES_PASSWORD:-ruze}@localhost:${POSTGRES_PORT:-5432}/${POSTGRES_DB:-ruze}`
- Redis: `redis://localhost:${REDIS_PORT:-6379}/0`

Health and lifecycle:
```bash
# Check status & health
docker compose ps

# Stop services
docker compose down

# Remove volumes/data (destructive)
docker compose down -v
```
