# How to Run LIMS Frontend

## Local Development
cd frontend
pnpm install
pnpm dev

Frontend: http://localhost:5173  
Backend: http://localhost:8000  

## Production Build
pnpm build

Serve with nginx or the existing Docker setup.

## Environment Variables
Development:
VITE_API_URL=http://localhost:8000

Production:
VITE_API_URL=/api

## Useful Commands
pnpm lint  
pnpm format  
pnpm test  
pnpm test:coverage