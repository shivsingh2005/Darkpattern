FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/*.config.js ./
COPY frontend/index.html ./

# Build
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built app from builder
COPY --from=0 /app/dist ./dist

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Start app
CMD ["serve", "-s", "dist", "-l", "3000"]
