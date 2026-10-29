# GETTHATFLAG — To-Do List

Private, single-user CTF training site. See `CLAUDE.md` for the decisions behind this plan.

**v1 is done when:** I can log in at my DuckDNS address, see the challenge board, solve one easy
challenge in each of the 4 categories, use hints, write a write-up, and see my score — with
nightly backups running.

---

## Phase 0 — Project setup
- [x] Add `.gitignore` (Python, `.env`, `db.sqlite3`, build outputs, `media/`)
- [x] Add `.env.example` listing every variable (Django secret, flags, DuckDNS token, backup keys) with dummy values
- [x] Add `README.md` with a short description and how to run locally
- [x] Set up Python project tooling (`pyproject.toml`, ruff, pytest)
- [x] Confirm `CLAUDE.md` is up to date

## Phase 1 — Django platform skeleton
- [x] Create Django project in `platform/`
- [x] Settings read from environment variables (django-environ or similar)
- [x] SQLite database
- [x] Tailwind CSS set up (standalone CLI, no Node required)
- [x] HTMX included
- [x] Base layout template — clean, modern style (TryHackMe-like)
- [x] App runs locally with one command

## Phase 2 — Login
- [ ] `accounts` app using Django's built-in auth
- [ ] Login / logout pages
- [ ] Every page requires login (except the login page)
- [ ] Rate-limit failed logins with django-axes
- [ ] Management command or docs for creating the single user
- [ ] Tests: anonymous user is redirected to login; lockout after repeated failures

## Phase 3 — Challenge data model
- [ ] `challenges` app with models:
  - [ ] `Category` (web, crypto, forensics, reversing)
  - [ ] `Challenge` (slug, title, category, difficulty, points, description, flag hash, files, container URL)
  - [ ] `Hint` (challenge, order, text)
  - [ ] `HintUnlock` (hint, unlocked_at)
  - [ ] `LearningPath` + ordered `PathStep` (suggested order, nothing locked)
  - [ ] `Solve` (challenge, solved_at, hints_used)
  - [ ] `WriteUp` (challenge, Markdown body, updated_at)
- [ ] Register models in the Django admin
- [ ] Tests for model basics

## Phase 4 — Challenge format & sync
- [ ] Define `challenges/_template/`:
  - [ ] `challenge.yaml` (slug, title, category, difficulty, points, description, hints, path + position)
  - [ ] `build.py` — reads the flag from the environment, generates downloadable files and/or the container
  - [ ] optional `Dockerfile` + `src/` for web challenges
  - [ ] `SOLUTION.md` — intended solution (honor system: don't read before solving)
- [ ] Flag naming convention in `.env` (e.g. `FLAG_WEB_01=GTF{...}`)
- [ ] `sync_challenges` management command: reads every `challenge.yaml`, runs `build.py`, stores the **hash** of the flag in the DB
- [ ] Generated files go to a git-ignored folder, served only to logged-in users
- [ ] Document how to add a challenge in `challenges/README.md`
- [ ] Tests: sync is idempotent; missing flag in `.env` fails loudly

## Phase 5 — Playing
- [ ] Challenge board grouped by category, showing solved / unsolved and points
- [ ] Learning paths page with suggested order per category
- [ ] Challenge detail page: description, downloads, link to live container (web)
- [ ] Flag submission (HTMX): hash + constant-time compare, correct/incorrect feedback
- [ ] Hints: unlock one at a time, free, recorded as used
- [ ] Score / progress page (total points, per-category progress, hints used)
- [ ] Tests: correct flag solves, wrong flag doesn't, flag is never sent to the browser, hint tracking

## Phase 6 — Write-ups
- [ ] Write-up editor on the challenge page (unlocked after solving)
- [ ] Markdown rendering with sanitising
- [ ] List of all my write-ups
- [ ] Tests: write-up saved and rendered safely

## Phase 7 — First 4 challenges (one easy per category)
- [ ] **Web 01** — e.g. hidden content / view-source or simple auth bypass (Docker container, ARM-compatible)
- [ ] **Crypto 01** — e.g. Caesar / Base64 chain (generated text file)
- [ ] **Forensics 01** — e.g. flag hidden in image metadata or appended data (generated file)
- [ ] **Reversing 01** — e.g. strings / simple password check binary (download only)
- [ ] Each has hints, a `SOLUTION.md`, and a place in a learning path
- [ ] Solve each one end-to-end locally

## Phase 8 — Deployment setup (local first)
- [ ] `deploy/docker-compose.yml`: Django (gunicorn), Caddy, web challenge containers
- [ ] Challenge containers on an internal network only — no access to the platform DB or secrets
- [ ] `deploy/Caddyfile`: HTTPS via DuckDNS, `forward_auth` to Django so challenge containers require login
- [ ] Static files served by Caddy / WhiteNoise
- [ ] Production settings: `DEBUG=False`, secure cookies, `ALLOWED_HOSTS`, HSTS
- [ ] Whole stack runs locally with Docker Compose

## Phase 9 — Oracle Always Free server (done in my Oracle account)
- [ ] Write step-by-step guide `deploy/ORACLE_SETUP.md`
- [ ] Create Oracle Cloud account and Always Free ARM VM (Ampere A1)
- [ ] Open ports 80/443 (Oracle security list + VM firewall), SSH key-only login
- [ ] Install Docker + Docker Compose
- [ ] Register DuckDNS subdomain and point it at the VM
- [ ] Copy `.env` to the server (never via git)
- [ ] Deploy, run `sync_challenges`, create my user
- [ ] Check HTTPS works and challenge containers are unreachable without login

## Phase 10 — Backups
- [ ] Nightly backup script: SQLite snapshot (`.backup`) → Oracle Object Storage (free tier)
- [ ] Cron job / systemd timer on the server
- [ ] Keep the last N backups
- [ ] Test a restore once

## v1 complete ✔
- [ ] Log in at DuckDNS URL → board → solve all 4 → hints → write-ups → score → backups confirmed

---

## Later (not v1)
- [ ] More challenges per path (easy → hard)
- [ ] Live pwn services (needs x86 emulation or an x86 host)
- [ ] Markdown export of write-ups
- [ ] Stats / streaks / badges
- [ ] Optional in-site AI tutor (Claude API with spend cap)
