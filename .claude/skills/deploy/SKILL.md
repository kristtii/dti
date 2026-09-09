---
name: deploy
description: Deploy blog_project to AWS Elastic Beanstalk. Use when preparing a release, building the deploy bundle, or changing deploy config.
---

Deploys to **AWS Elastic Beanstalk** (gunicorn + Postgres).

## Pre-deploy checklist
1. Dependencies pinned: `pip freeze > requirements.txt` (current pins: Django 6.0.6, gunicorn, psycopg2-binary, python-dotenv).
2. Collect static: `python manage.py collectstatic` → `staticfiles/` (committed for EB).
3. `DEBUG = False` in `settings.py` (already set). Confirm before shipping.
4. Migrations applied against the target Postgres.

## EB config
- `.ebextensions/django.config`:
  - `WSGIPath: blog_project.wsgi:application`
  - `DJANGO_SETTINGS_MODULE: blog_project.settings`
- Bundle artifact: `deploy.zip` (project files + `staticfiles/`, excluding venv/db).

## Environment variables
- Set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` in the **EB console** (Configuration → Software → Environment properties), NOT in committed files.
- Local `.env` is for development only and must not ship in `deploy.zip`.

## Security warnings to surface
- `SECRET_KEY` is hardcoded in `settings.py` — move to `os.getenv('SECRET_KEY')` and set it as an EB env var before a real production deploy.
- `ALLOWED_HOSTS = ['*']` — tighten to the EB domain for production.

## STRICT (CLAUDE.md)
- Never edit `.env` — instruct the user. Never modify db files directly. Ask before changing existing files.
