# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

GETTHATFLAG is a **private, single-user** Capture the Flag (CTF) training site. The owner is an
experienced coder who is new to security, and is also using this project to learn agentic coding
with Claude Code. Work through `TODO.md` phase by phase and tick items off as they are completed.

- One user only: no sign-up, no multi-user features, no public scoreboard.
- Four categories: **web**, **crypto**, **forensics/stego**, **reversing**.
- Reversing challenges are **download-only** (no live pwn services in v1).
- Learning paths per category show a **suggested order**; nothing is locked.
- Hints unlock one at a time, are **free**, and are recorded as used.
- The owner writes a Markdown **write-up** after solving each challenge.
- No in-site AI tutor. The owner asks Claude directly when stuck.

## Tech stack

| Area | Choice |
|---|---|
| Platform | Django, server-rendered templates, HTMX, Tailwind (standalone CLI, no Node) |
| Database | SQLite |
| Auth | Django built-in login + django-axes rate limiting |
| Challenges | Web = Docker containers; others = generated downloadable files |
| Proxy | Caddy: automatic HTTPS + `forward_auth` to Django to protect challenge containers |
| Hosting | Oracle Always Free **ARM64** VM, Docker Compose |
| Domain | DuckDNS free subdomain |
| Backups | Nightly SQLite backup to Oracle Object Storage |
| Budget | ~$0/month. Do not add paid services. |

## Repository layout

```
platform/        Django project (apps: accounts, challenges)
challenges/      One folder per challenge, plus _template/
deploy/          docker-compose.yml, Caddyfile, backup script, ORACLE_SETUP.md
TODO.md          The build plan, checked off as work completes
.env.example     Every env var with dummy values
```

## Hard rules

1. **Never commit flags or secrets.** The repo is public. Real flags live only in `.env` on the
   server (`FLAG_<CATEGORY>_<NN>=GTF{...}`). Don't put a real flag in code, YAML, tests, fixtures,
   generated files, commit messages or docs. Tests use obviously fake flags like `GTF{test}`.
2. **Store only flag hashes in the database.** Compare submissions in constant time
   (`hmac.compare_digest`). Never send a flag to the browser.
3. **Files containing flags are generated, never committed.** Each challenge's `build.py` reads
   its flag from the environment and writes output to a git-ignored build folder.
4. **Isolate challenge containers.** They run on an internal Docker network, can only be reached
   through Caddy after a successful Django auth check, and get no access to the platform DB,
   `.env` or other secrets. Assume every challenge will be compromised.
5. **Intentional vulnerabilities belong only inside `challenges/`.** The platform code in
   `platform/` must be secure: CSRF on, sanitised Markdown, login required on every page except
   login, production settings with `DEBUG=False` and secure cookies.
6. **Containers must build for ARM64** (`linux/arm64`). Avoid x86-only base images or binaries.
7. **Keep it free.** Don't introduce dependencies or services that cost money.

## Adding a challenge

When asked for a new challenge (e.g. "make an easy SQLi challenge"):

1. Copy `challenges/_template/` to `challenges/<category>-<NN>-<short-name>/`.
2. Fill in `challenge.yaml`: slug, title, category, difficulty, points, description, ordered
   hints, learning path and position.
3. Write `build.py` to read `FLAG_<CATEGORY>_<NN>` from the environment and produce the
   downloadable files and/or container.
4. For web challenges, add a `Dockerfile` and `src/`.
5. Write `SOLUTION.md` with the intended solution path. The owner follows an honor system and
   won't read it before solving.
6. Add the new flag variable (dummy value) to `.env.example`.
7. Run `sync_challenges` locally and solve the challenge end to end to check it works.

Pitch difficulty for someone new to security: easy challenges teach one concept, and hints go
from a gentle nudge to nearly the answer.

## Conventions

- Python formatted and linted with **ruff**. Tests use **pytest** (pytest-django).
- Add or update tests for platform behaviour, especially flag checking, auth and hint tracking.
- Settings come from environment variables. No hard-coded secrets or hostnames.
- Keep the UI clean and modern (TryHackMe-like), and server-rendered with HTMX for interactivity.
  No SPA framework.
- Prefer Django built-ins (auth, admin, management commands) over new dependencies.
- Explain security concepts briefly in code review notes or replies when relevant. The owner is
  learning.

## Commands

Fill these in as the project is scaffolded:

```bash
# run locally
# run tests
# lint / format
# sync challenges
# full stack via Docker Compose
```
