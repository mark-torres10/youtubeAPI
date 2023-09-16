# Use Node.js 14 as the base image
FROM node:14

# Set environment variables
ENV NODE_ENV=production

# Create a directory for the app
WORKDIR /app

# Copy the frontend source code into the container
COPY src/frontend/package.json src/frontend/package-lock.json /app/
COPY src/frontend /app/src/frontend

# Install dependencies
RUN npm install --production

# Expose the port your app runs on (adjust as needed)
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
