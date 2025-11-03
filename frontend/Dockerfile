FROM node:20-slim

WORKDIR /app

# Install pnpm and curl for healthcheck
RUN npm install -g pnpm && \
    apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install

# Copy application code
COPY . .

# Expose port
EXPOSE 5173

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5173/ || exit 1

# Start development server
CMD ["pnpm", "dev", "--host"]
