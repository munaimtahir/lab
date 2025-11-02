# Backend

Django-based backend service.

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development

### Run migrations
```bash
python manage.py migrate
```

### Run development server
```bash
python manage.py runserver
```

### Run tests
```bash
pytest
```

### Run tests with coverage
```bash
pytest --cov=. --cov-report=term-missing --cov-report=html
```

### Linting and formatting

```bash
# Format code
black .
isort .

# Lint code
ruff check .

# Type check
mypy .
```

## Project Structure

- `core/` - Django project settings
- `health/` - Health check app
