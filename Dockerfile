# Use the official Node.js LTS image
FROM node:20-slim

# Create and set the working directory
WORKDIR /app

# Copy package files first (for better layer caching)
COPY server/package*.json ./

# Install dependencies
RUN npm ci --production

# Copy the server code
COPY server/ ./

# Copy the download folder (for static serving)
COPY download/ /app/download/

# Expose the port the server runs on
ENV PORT=3001
EXPOSE 3001

# Run as a non-root user for security
USER node

# Start the server
CMD ["node", "server.js"]
