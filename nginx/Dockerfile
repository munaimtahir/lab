# Stage 1: Build the frontend
FROM node:20-slim AS builder

WORKDIR /app

# Install pnpm (matching version from frontend/package.json)
RUN npm install -g pnpm@8.15.9

# Copy frontend package files
COPY frontend/package.json frontend/pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy frontend application code
COPY frontend/ ./

# Create .env for production build with relative API path
# In production, nginx proxies /api/* to backend:8000 internally
# This ensures the frontend uses the relative path /api for all API calls
RUN echo "VITE_API_URL=/api" > .env

# Build the application (creates dist directory)
RUN pnpm build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built frontend files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 443

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# nginx runs in foreground by default
CMD ["nginx", "-g", "daemon off;"]
