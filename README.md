# lab
Laboratory Information Management System

## Mono-Repo Structure

This project is organized as a mono-repo with the following structure:

- **backend/** - Django-based backend API with pytest, factory_boy, freezegun, ruff, mypy, black, isort
- **frontend/** - Vite + React + TypeScript frontend with ESLint, Prettier, Vitest + RTL, Playwright
- **infra/** - Infrastructure as Code and deployment configurations
- **docs/** - Project documentation and guides

## Quick Start

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest --cov=. --cov-report=term-missing
```

### Frontend Tests
```bash
cd frontend
npm run test:coverage
```

## Pre-commit Hooks

This project uses pre-commit hooks for code quality. To set up:

```bash
pip install pre-commit
pre-commit install
```

The hooks will automatically run on git commit and check:
- Python: black, isort, ruff, mypy
- JavaScript/TypeScript: prettier, eslint

