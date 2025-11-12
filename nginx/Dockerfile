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

# Production API URL configuration
# ARG allows override at build time: docker build --build-arg VITE_API_URL=/api
# Default: /api (nginx proxies /api/* to backend:8000 internally)
# This ensures the frontend uses the correct API path for the deployment environment
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

# Create .env for production build
RUN echo "VITE_API_URL=${VITE_API_URL}" > .env

# Build the application in production mode (creates dist directory)
# Uses .env.production and the VITE_API_URL env var set above
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
