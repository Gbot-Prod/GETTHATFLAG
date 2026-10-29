# GETTHATFLAG

A private, single-user Capture the Flag (CTF) training site: web, crypto, forensics and
reversing challenges, organised into learning paths, with hints and personal write-ups.
Built with Django + HTMX + Tailwind, as a project for learning agentic coding with Claude Code.

- Build plan: [`TODO.md`](TODO.md)
- Project rules and conventions: [`CLAUDE.md`](CLAUDE.md)

## Run locally

Requirements: [uv](https://docs.astral.sh/uv/), `make`, `curl`.

```bash
make setup   # install deps, Tailwind CLI, copy .env.example -> .env, migrate
make user    # create your login (the single owner account)
make dev     # build CSS and start http://127.0.0.1:8000
```

Edit `.env` and set `DJANGO_SECRET_KEY` to a long random string.

## Other commands

```bash
make test       # pytest
make lint       # ruff check + format check
make format     # auto-fix lint + format
make css-watch  # rebuild Tailwind CSS on template changes
```
