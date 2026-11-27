# Kanmind Backend

REST API for Kanban-style task management. Board, column, and card operations with JWT auth, cursor-based pagination, and Redis-backed rate limiting. Built for frontend teams who need a lean, well-documented backend.

[![build](https://img.shields.io/github/actions/workflow/status/USER/REPO/ci.yml?label=build)](https://github.com/USER/REPO/actions)
[![version](https://img.shields.io/github/v/release/USER/REPO)](https://github.com/USER/REPO/releases)
[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Quickstart

**Prerequisites:** Node.js 20+, PostgreSQL 16, Redis 7

```bash
git clone https://github.com/USER/REPO.git && cd REPO
npm install
cp .env.example .env
docker compose up -d
npm run migrate && npm run seed
npm run dev
```

Server live at `http://localhost:3000` · Health: `GET /health`

<details>
<summary>Without Docker?</summary>

→ [docs/setup-native.md](docs/setup-native.md) (macOS / Linux / WSL2)

</details>

## Usage

### Configuration

All settings via environment variables (full list in `.env.example`):

| Variable | Required | Purpose |
|----------|----------|---------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `REDIS_URL` | Yes | Cache + rate limiting |
| `JWT_SECRET` | Yes | Access token signing (256-bit) |
| `JWT_REFRESH_SECRET` | Yes | Refresh token signing |
| `PORT` | No | HTTP port (default `3000`) |
| `RATE_LIMIT_MAX` | No | Requests/min per user (default `100`) |

### Authentication

```bash
# Login → { access_token, refresh_token }
curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"…","password":"…"}'

# Authenticated request
curl http://localhost:3000/api/v1/boards \
  -H "Authorization: Bearer <access_token>"
```

Access tokens expire in **15 min**. Rotate via `POST /auth/refresh`.

### Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/auth/register` | – | Create user |
| `POST` | `/auth/login` | – | Get tokens |
| `POST` | `/auth/refresh` | – | Rotate access token |
| `GET` | `/boards` | Bearer | List boards (paginated) |
| `POST` | `/boards` | Bearer | Create board |
| `GET` | `/boards/:id` | Bearer | Board with columns + cards |
| `POST` | `/boards/:id/columns` | Bearer | Add column |
| `POST` | `/columns/:id/cards` | Bearer | Add card |
| `PATCH` | `/cards/:id` | Bearer | Move / update card |
| `DELETE` | `/cards/:id` | Bearer | Delete card |

**Error format (global):**
```json
{ "error": { "code": "VALIDATION_ERROR", "message": "…", "details": [] } }
```

→ [Full API reference](docs/api.md)

### Modifying the codebase

- **New module:** create `src/modules/<name>/` → controller, service, repository, schema, routes. Mount in `src/routes/index.ts`.
- **New migration:** `npm run migrate:create -- -n <name>` → edit → `npm run migrate`.
- **Rate limits:** edit `src/middleware/rate-limit.ts` or set `RATE_LIMIT_MAX`.

## Project Structure

```
src/
├── config/          # Env validation, DB + Redis connections
├── middleware/      # Auth, rate limiting, error handler, request logger
├── modules/         # board, column, card, user, auth
├── routes/          # Top-level router
├── utils/           # Pagination, async handler
├── migrations/      # SQL migrations
├── seeds/           # Seed scripts
└── app.ts           # Fastify instance, listen
tests/
├── unit/
├── integration/
└── fixtures/
```

## Tests

```bash
npm test              # Unit (no external deps)
npm run test:int      # Integration (requires Docker)
npm run test:cov      # Coverage
```

Unit: services + utils. Integration: full HTTP stack against real Postgres + Redis.

## Notes

- Pagination is **cursor-based** – use `?cursor=<next_cursor>` from the response.
- API is versioned under `/api/v1`. Breaking changes → `/api/v2`.
- All timestamps are UTC, ISO 8601.

## Contributing

PRs against `main`. Conventional Commits (`feat:`, `fix:`, `refactor:`). `npm run lint && npm test` must pass. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)   