.PHONY: setup css css-watch dev test lint format user

TAILWIND = bin/tailwindcss -i platform/static_src/input.css -o platform/static/css/app.css
MANAGE = uv run python platform/manage.py

## First-time setup: install deps, Tailwind, create DB
setup:
	uv sync
	[ -f .env ] || cp .env.example .env
	[ -x bin/tailwindcss ] || scripts/install-tailwind.sh
	$(MAKE) css
	$(MANAGE) migrate

css:
	$(TAILWIND) --minify

css-watch:
	$(TAILWIND) --watch

## Run the dev server (rebuilds CSS once first)
dev: css
	$(MANAGE) runserver

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

## Create the single owner account (also gives access to /admin/)
user:
	$(MANAGE) createsuperuser
