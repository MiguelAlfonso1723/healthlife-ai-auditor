# 🤝 Contributing Guide

## Branch Strategy

Never work directly on:

- main
- develop

Create a feature branch.

Example

feature/data-cleaning

feature/api-validation

feature/dashboard

---

# Workflow

Issue

↓

Create Branch

↓

Develop

↓

Commit

↓

Push

↓

Pull Request

↓

Review

↓

Merge into develop

---

# Commit Convention

feat:

fix:

docs:

refactor:

test:

chore:

Example

feat(ai): train first validation model

---

# Pull Requests

Every Pull Request must:

- Reference an Issue
- Pass all tests
- Update documentation if required
- Be reviewed before merging

---

# Labels

Always assign:

Phase

Area

Priority

Type

---

# Project Board

Backlog

↓

Ready

↓

In Progress

↓

Review

↓

Testing

↓

Done

---

# Coding Standards

- Use descriptive variable names.
- Keep functions small.
- Add comments only when necessary.
- Follow project folder structure.

---

# Documentation

Every new feature should update the corresponding documentation when necessary.

---

# AI Development

All experiments must be performed inside notebooks.

Production code belongs inside src/.

---

# Backend

Business logic must never be implemented inside API endpoints.

Endpoints should only orchestrate requests.

---

# Dashboard

Dashboard must consume the REST API.

Never access datasets directly from the UI.