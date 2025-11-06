# Frontend Dockerfile for Beyond Words PWA
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package files
COPY beyond-words-web/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY beyond-words-web/ ./

# Build the app
RUN npm run build

# Production stage - serve with nginx
FROM nginx:alpine

# Copy built files
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
