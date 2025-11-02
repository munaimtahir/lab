# LIMS — Lab Information Management System (Dev Pack v0)
**Date:** 2025-11-02

This repository is a *code-free* starter kit: it contains documents, CI skeletons, and structure for an AI agent (or human team) to build a full-stack LIMS in stages with 100% test coverage.
The actual application code will be generated later using the stage prompts in `docs/AGENT.md` and `docs/TASKS.md`.

## Structure
- `docs/` — specifications, prompts, checklists
- `backend/` — (empty now) Python/Django target with pytest
- `frontend/` — (empty now) React + TypeScript target with Vitest + Playwright
- `infra/` — docker-compose and environment examples
- `.github/workflows/` — CI pipeline scaffold

Start by reading `docs/SETUP.md` then `docs/GOALS.md`, and finally run the prompts in `docs/AGENT.md` stage-by-stage.
