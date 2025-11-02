# Frontend

React + TypeScript frontend powered by Vite.

## Setup

```bash
cd frontend
npm install
```

## Development

### Run development server
```bash
npm run dev
```

### Build for production
```bash
npm run build
```

### Run unit tests
```bash
npm test
```

### Run tests with coverage
```bash
npm run test:coverage
```

### Run Playwright e2e tests
```bash
# First install browsers
npm run playwright:install

# Then run tests
npm run playwright
```

### Linting and formatting

```bash
# Format code
npm run format

# Check formatting
npm run format:check

# Lint code
npm run lint
```

## Project Structure

- `src/` - Source code
  - `Health.tsx` - Health component
  - `Health.test.tsx` - Health component tests
  - `test/` - Test utilities
- `e2e/` - Playwright end-to-end tests
