# Al-Shifa LIMS Frontend

Modern React + TypeScript + Vite frontend for the Al-Shifa Laboratory Information Management System.

## Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS
- **React Router 7** - Client-side routing
- **React Query (TanStack Query)** - Data fetching and caching
- **Vitest + React Testing Library** - Unit testing
- **Playwright** - E2E testing

## Getting Started

### Prerequisites

- Node.js 20+
- pnpm (recommended) or npm

### Installation

```bash
cd frontend
pnpm install
```

### Development

```bash
# Start dev server (http://localhost:5173)
pnpm dev

# Run tests
pnpm test

# Run tests with UI
pnpm test:ui

# Run tests with coverage
pnpm test:coverage

# Lint code
pnpm lint

# Format code
pnpm format

# Build for production
pnpm build

# Preview production build
pnpm preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   │   └── ProtectedRoute.tsx
│   ├── hooks/          # Custom React hooks
│   │   └── useAuth.tsx
│   ├── layouts/        # Layout components
│   │   └── MainLayout.tsx
│   ├── pages/          # Page components
│   │   ├── home/
│   │   ├── lab/
│   │   ├── settings/
│   │   └── LoginPage.tsx
│   ├── services/       # API client and services
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── patients.ts
│   │   ├── catalog.ts
│   │   └── orders.ts
│   ├── types/          # TypeScript type definitions
│   │   └── index.ts
│   ├── utils/          # Utility functions
│   │   ├── constants.ts
│   │   └── validators.ts
│   └── test/           # Test setup
│       └── setup.ts
├── e2e/                # Playwright E2E tests
├── public/             # Static assets
└── dist/               # Production build output
```

## Key Features

### Authentication
- JWT-based authentication with automatic token refresh
- Role-based access control (RBAC)
- Protected routes with role validation
- Secure token storage with localStorage

### Lab Workflow
- **New Lab Slip**: Patient registration and test selection
- **Worklist**: Filtered order list with status tracking
- **Order Detail**: Comprehensive view with tabs for samples, results, and reports

### Patient Management
- Auto-suggest for existing patients by CNIC or phone
- Validation for Pakistani CNIC and phone formats
- Automatic age calculation from date of birth

### Test Selection
- Dynamic test catalog search
- Real-time pricing calculation
- Discount and payment tracking

### UI/UX
- Responsive design (mobile, tablet, desktop)
- Color-coded status indicators
- Loading states and error handling
- Dark red header matching xMed EMR branding

## Routes

| Route | Description | Access |
|-------|-------------|--------|
| `/` | Dashboard/Home | Authenticated users |
| `/login` | Login page | Public |
| `/lab` | Lab home with action tiles | Authenticated users |
| `/lab/new` | New lab slip form | Reception, Admin |
| `/lab/worklist` | Order worklist | Phlebotomy, Technologist, Pathologist, Admin |
| `/lab/orders/:id` | Order detail page | Authenticated users |
| `/settings` | Settings home | Admin only |

## Authentication Flow

1. User logs in with username/password
2. Backend returns access token (15 min) and refresh token (7 days)
3. Access token is attached to all API requests via Authorization header
4. On 401 response, client automatically refreshes token
5. If refresh fails, user is redirected to login

## Role-Based Permissions

### Reception
- Patient registration
- Order creation
- Basic reports viewing

### Phlebotomy
- Sample collection
- Worklist viewing

### Technologist
- Sample receiving
- Result entry
- Worklist viewing

### Pathologist
- Result verification
- Result publishing
- Report generation
- Worklist viewing

### Admin
- Full access to all features
- Settings management

## Testing

### Unit Tests (Vitest)
```bash
# Run all tests
pnpm test

# Run with coverage
pnpm test:coverage

# Watch mode
pnpm test:watch
```

Current coverage: **60 tests passing**

### E2E Tests (Playwright)
```bash
# Install browsers
pnpm playwright:install

# Run E2E tests
pnpm playwright
```

## API Integration

The frontend communicates with the Django backend API:

```typescript
// API client automatically handles:
// - Token attachment
// - Token refresh
// - Error handling
// - Request/response transformation

import { apiClient } from './services/api'

// GET request
const data = await apiClient.get<Type>('/api/endpoint/')

// POST request
const result = await apiClient.post<Type>('/api/endpoint/', { data })
```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
# Default VPS deployment
VITE_API_BASE_URL=http://172.235.33.181:8000

# Local development override
# VITE_API_BASE_URL=http://localhost:8000

# When the frontend is served behind the same domain and nginx proxies /api/
# VITE_API_BASE_URL=/api
```

## Color Palette

Matching the existing xMed EMR design:

- **Header**: Dark red (`bg-red-900`)
- **Section bars**: Blue (`bg-blue-700`)
- **Cards**: Teal (`bg-teal-50`)
- **Status badges**: Context-based (NEW=blue, COLLECTED=yellow, etc.)

## Validation Rules

### CNIC
- Format: `#####-#######-#`
- Example: `12345-1234567-1`

### Phone
- Pakistani mobile format
- Accepted: `03001234567`, `+923001234567`

### Date of Birth
- Must not be in the future
- Automatically calculates age in years, months, or days

## Future Enhancements

- [ ] Full sample management workflow
- [ ] Results entry interfaces
- [ ] PDF report generation
- [ ] Bulk upload functionality
- [ ] Advanced filtering and search
- [ ] User management UI
- [ ] Real-time notifications
- [ ] Offline support
- [ ] Print queue management

## Troubleshooting

### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Clear Vite cache
rm -rf node_modules/.vite
```

### Test Failures

```bash
# Update test snapshots
pnpm test -- -u

# Run specific test file
pnpm test -- src/path/to/test.test.tsx
```

## Contributing

1. Follow existing code style and patterns
2. Write tests for new features
3. Run linter and formatter before committing
4. Keep components small and focused
5. Use TypeScript strict mode
6. Document complex logic

## License

Copyright © 2024 Al-Shifa Laboratory
