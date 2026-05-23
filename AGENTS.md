# AGENTS.md

## Scope

These instructions apply to the whole workspace. Use them with the path-scoped files in `.github/instructions/`.

## Repository Shape

- `blindtest/` is the Django 6 backend. It exposes REST endpoints under `/v1/`, GraphQL under `/v1/graphql/`, websocket consumers through Channels, and async jobs through Celery.
- `mainsite/` is the Nuxt 4 application. It talks to the backend over HTTP and websockets and uses selective SSR through `routeRules`.
- `docker-compose.yaml` documents the deployed service wiring and the backend container port.

## First References

- Start with [README.md](README.md) for the product overview and high-level architecture.
- Use [mainsite/README.md](mainsite/README.md) for product concepts such as tables, relationships, triggers, functions, and constraints.
- Use [docker-compose.yaml](docker-compose.yaml) when you need deployment domains, env files, or mounted paths.

## Working Commands

- Backend dev server: `cd blindtest && python manage.py runserver`
- Backend tests: `cd blindtest && pytest`
- Frontend dev server: `cd mainsite && pnpm dev`
- Frontend unit tests: `cd mainsite && pnpm test:unit`
- Frontend Nuxt tests: `cd mainsite && pnpm test:nuxt`
- Frontend e2e tests: `cd mainsite && pnpm test:e2e`
- Frontend lint: `cd mainsite && pnpm lint`

## Repo Conventions

- Keep backend API changes versioned under `/v1/`.
- Treat Django model changes as cross-cutting: check the app's `api/`, `graphql/`, `tests/`, and websocket or task modules when relevant.
- Preserve REST and GraphQL behavior together when a backend domain model changes.
- Do not change websocket authentication or ASGI wiring casually. Read the existing backend websocket setup before touching it.
- Keep frontend changes aligned with the backend domain language from the README files: databases contain tables, and table behavior includes relationships, triggers, functions, constraints, and windows.

## Validation Strategy

- Prefer focused validation from the touched area before running broad suites.
- For backend-only changes, run `pytest` from `blindtest/`.
- For frontend-only changes, run the narrowest matching script from `mainsite/package.json`.
