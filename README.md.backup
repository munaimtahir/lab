# LIMS — Lab Information Management System

![CI](https://github.com/munaimtahir/lab/workflows/CI/badge.svg)

A production-ready Laboratory Information Management System (LIMS) built with Django REST Framework and React.

## 🏗️ Architecture

- **Backend**: Python 3.12, Django 5.x, Django REST Framework, PostgreSQL 16, Redis 7
- **Frontend**: React 19, TypeScript, Vite, TailwindCSS
- **Authentication**: JWT with role-based access control
- **Infrastructure**: Docker Compose, GitHub Actions CI/CD

## 📊 Features Implemented

### Backend (96% Test Coverage - 29 tests passing)
- ✅ **Authentication**: JWT-based auth with token blacklisting
- ✅ **User Management**: Role-based access (Admin, Reception, Phlebotomy, Technologist, Pathologist)
- ✅ **Patient Registration**: Full demographics with validation (CNIC, phone, DOB)
- ✅ **Test Catalog**: Manage available lab tests
- ✅ **Order Management**: Create and track test orders
- ✅ **Seed Data**: Demo users and test catalog

### Frontend
- ✅ Basic UI structure with TailwindCSS
- ✅ Login/Logout flow
- ✅ Dashboard layout
- 🔄 Patient registration form (to be completed)
- 🔄 Order creation workflow (to be completed)

### Not Yet Implemented
- Sample collection with barcode generation
- Results entry and verification workflow
- PDF report generation with Al Shifa template
- Complete frontend pages with React Query
- E2E Playwright tests
- Full 100% test coverage

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- pnpm
- Docker & Docker Compose (optional)

### Local Development

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

#### Frontend Setup
```bash
cd frontend
pnpm install
pnpm dev
```

### Docker Setup
```bash
cd infra
docker-compose up
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest -v --cov=.
```

Current coverage: **96.36%** with 29 passing tests

### Frontend Tests
```bash
cd frontend
pnpm test
```

## 👥 Default Users

After running `python manage.py seed_data`:

- **admin** / admin123 (Admin)
- **reception** / reception123 (Reception)
- **tech** / tech123 (Technologist)
- **pathologist** / path123 (Pathologist)

## 📚 API Endpoints

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout

### Patients
- `GET /api/patients/` - List/search patients
- `POST /api/patients/` - Create patient
- `GET /api/patients/:id/` - Get patient details

### Catalog
- `GET /api/catalog/` - List test catalog
- `GET /api/catalog/:id/` - Get test details

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `GET /api/orders/:id/` - Get order details

## 🔧 Configuration

Environment variables are configured in `.env` file:
- `DJANGO_SECRET_KEY` - Django secret key
- `POSTGRES_*` - PostgreSQL connection settings
- `REDIS_URL` - Redis connection URL
- `VITE_API_BASE` - Frontend API base URL

## 📝 Development Status

This is a **partial implementation** of the full LIMS specification. The foundation is solid with:
- Robust authentication and authorization
- Well-tested patient and order management
- Clean architecture following Django/DRF best practices
- Docker-ready containerization

**Remaining work** includes:
- Sample collection and tracking
- Results entry and verification
- PDF report generation
- Complete frontend implementation
- E2E testing suite
- Achieving 100% test coverage

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

See `docs/CONTRIBUTING.md` for contribution guidelines.

