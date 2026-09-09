# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Django 6.0 blog app. Single app `blog` inside project `blog_project`. Function-based views, email-verified registration, post CRUD with likes, search, category filter. Deploys to AWS Elastic Beanstalk (gunicorn + Postgres).

## Commands

Run from repo root (dir containing `manage.py`).

```bash
python manage.py runserver          # dev server
python manage.py migrate            # apply migrations
python manage.py makemigrations     # create migrations after model change
python manage.py createsuperuser    # admin user
python manage.py collectstatic      # gather static -> staticfiles/ (needed for EB deploy)
python manage.py test               # run all tests
python manage.py test blog.tests.ClassName.test_method   # single test
```

## STRICT USE
Always use Self expaining Human Written Code & Variable names
Do NOT comment unless absolutely neccessary
Always ask before changing content in a file
Never use hard-coded secrects always use .env with os.getenv()
Never edit yourself .env file always instruct me to edit .env
Never modify db files directly

## Environment

`.env` (loaded via python-dotenv in settings.py) must define:
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — Postgres (no SQLite fallback; `db.sqlite3` in repo is stale/unused)
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` — Gmail SMTP app password (port 587 TLS) for verification emails

App will not boot without DB env vars set.

## Architecture

**Models (`blog/models.py`)**
- `Category` — name + unique slug.
- `Post` — slug-keyed (URLs use slug not pk), FK to Category, FK to User (`author`), M2M `likes` to User. Has legacy `author_name` CharField kept alongside the `author` FK. `is_published` gates public visibility.
- `EmailVerification` — OneToOne User, uuid `token`, `is_expired()` = older than 5 min.

**Auth flow (registration is custom, login/logout is Django built-in)**
- `blog_project/urls.py` includes `django.contrib.auth.urls` at `/accounts/` (login/logout used; password change/reset not used).
- Registration (`register_view`): creates user with `is_active=False`, generates uuid token, emails `verify_email` link. User cannot log in until they click link within 5 min. `verify_email` sets `is_active=True` and deletes the token row. Expired token -> `verification_failed.html`.
- Redirect targets in `settings.py`: `LOGIN_REDIRECT_URL=post_list`, `LOGOUT_REDIRECT_URL=home`, `LOGIN_URL=login`.

**Views (`blog/views.py`)** — all function-based. Ownership check pattern: `edit_post`/`delete_post`/ redirect to `post_detail` if `post.author != request.user`. Mutating views (`create/edit/delete/my_posts/like`) use `@login_required`.

**URL name gotcha**: the URL is named `post_detail` (singular) in `blog/urls.py`; views `redirect('post_detail', ...)`. Don't confuse with the `post_list` view/page.

**Templates** — two roots: project-level `templates/` (base.html, 404.html, registration/login.html) + app-level `blog/templates/blog/`. `APP_DIRS=True` plus `DIRS=[BASE_DIR/'templates']`.

**Static** — sources in `static/`, collected into `staticfiles/` (`STATIC_ROOT`). `staticfiles/` is committed for EB deploys.

## Deploy (AWS Elastic Beanstalk)

`.ebextensions/django.config` sets `WSGIPath=blog_project.wsgi:application` and `DJANGO_SETTINGS_MODULE`. `deploy.zip` is the bundled artifact. gunicorn is the prod server.

## Notes / known rough edges

- `SECRET_KEY` is hardcoded in settings.py; `DEBUG=False`, `ALLOWED_HOSTS=['*']`.
- Source comments are in Albanian — fine to read, write new code/comments in English.
