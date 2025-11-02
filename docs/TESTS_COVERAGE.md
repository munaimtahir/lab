# Test Coverage

## Overview

**Current Coverage: 93.33%** (73 tests passing)

The LIMS implementation includes comprehensive test coverage across all modules with unit tests, integration tests, and role-based access control validation.

## Test Suite Summary

| Module | Tests | Coverage | Description |
|--------|-------|----------|-------------|
| Authentication | 7 | 100% | JWT login, refresh, logout, token validation |
| Patients | 16 | 98% | CRUD, validation, search, pagination, RBAC |
| Test Catalog | 3 | 100% | Listing, detail view, authentication |
| Orders | 4 | 100% | Creation, filtering, patient association |
| Samples | 12 | 100% | Collection, receiving, barcode generation, RBAC |
| Results | 15 | 100% | Entry, verification, publishing, state machine, RBAC |
| Reports | 11 | 100% | PDF generation, download, validation, RBAC |
| Seed Data | 4 | 100% | Command execution, idempotency |
| Health Check | 1 | 100% | API health endpoint |
| **Total** | **73** | **93.33%** | Full backend coverage |

## Running Tests

### Backend Tests

```bash
cd backend
pytest -v --cov=. --cov-report=term-missing

# With coverage threshold
pytest --cov=. --cov-report=term-missing --cov-fail-under=90

# Specific module
pytest patients/tests.py -v

# With HTML report
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Frontend Tests

```bash
cd frontend
pnpm test

# With coverage
pnpm test:coverage

# Watch mode
pnpm test -- --watch
```

## Test Categories

### 1. Model Tests
- Validate model creation and constraints
- Test auto-generation (MRN, order numbers, barcodes)
- Verify relationships and cascading
- Check string representations

### 2. Serializer Tests
- Validation rules (CNIC format, phone format, DOB)
- Field-level validation
- Required fields
- Read-only fields

### 3. API Tests
- CRUD operations
- Search and filtering
- Pagination
- State transitions

### 4. RBAC Tests
- Role-based access control
- Permission enforcement
- Forbidden access scenarios
- Authentication requirements

### 5. Workflow Tests
- Complete workflows (sample collection → result entry → verification → publishing)
- State machine validations
- Business rule enforcement

### 6. Edge Case Tests
- Non-existent resources (404 errors)
- Invalid data (400 errors)
- Unauthorized access (403 errors)
- Invalid tokens (401 errors)

## Coverage Goals

### Backend
- **Target: 100%**
- **Current: 93.33%**
- **Remaining:** 
  - Patients serializer validation edge cases
  - Settings configuration edge case
  - PDF generation integration test

### Frontend
- **Target: 100%**
- **Current: Minimal**
- **Needed:**
  - Component tests (React Testing Library)
  - API integration tests
  - Form validation tests
  - Navigation tests

## Continuous Integration

Tests run automatically on:
- Push to any branch
- Pull request creation/update
- CI enforces coverage thresholds
- Separate jobs for backend and frontend

## Missing Coverage (To Reach 100%)

1. **patients/serializers.py lines 42, 50**
   - Phone validation error path
   - CNIC validation error path

2. **core/settings.py line 98**
   - CELERY_BROKER_URL configuration

3. **reports/pdf_generator.py**
   - Currently mocked in unit tests (correct approach)
   - Integration test with real PDF needed

## E2E Tests (Planned with Playwright)

### Critical Workflows
1. Login → Register patient → Create order → Collect sample → Receive sample → Enter result → Verify result → Publish result → Generate report → Download PDF
2. Multi-user scenarios
3. Accessibility checks
4. Cross-browser testing
