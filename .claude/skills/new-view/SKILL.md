---
name: new-view
description: Create a new Django page (view + URL + template) following blog_project conventions. Use when the user asks for a new view, page, or screen.
---

This project uses **function-based views** only (`blog/views.py`). Follow these steps.

## 1. View — `blog/views.py`
- Write a function view. Use a clear, self-explaining name (no comments unless the logic is non-obvious — see STRICT USE in CLAUDE.md).
- Read data with `get_object_or_404` and slug lookups, never raw pk.
- Add `@login_required` if the page mutates data or is owner-only.
- Ownership pattern when editing/deleting a Post:
  ```python
  if post.author != request.user:
      return redirect('post_detail', slug=post.slug)
  ```
- For forms, use a `ModelForm` from `blog/forms.py`; on `create`, set `post.author = request.user` before `save()`.

## 2. URL — `blog/urls.py`
- Add a `path()` with a clear `name`.
- The detail route name is `post_detail` (singular) — match existing names, do not invent variants.
- Place `<slug:slug>` routes AFTER static segment routes (e.g. `posts/create/` before `posts/<slug:slug>/`) so the slug doesn't swallow them.

## 3. Template — `blog/templates/blog/<name>.html`
- `{% extends "base.html" %}`.
- Fill `{% block title %}` and `{% block content %}`.
- Reuse existing CSS classes: `container`, `main-content`, `form-card`, `nav-links`.
- Use `{% url 'name' %}` for all links.
- Every POST form needs `{% csrf_token %}`.

## STRICT
- Ask before editing existing files.
- Never hardcode secrets — use `.env` + `os.getenv()`.
