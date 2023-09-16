# Use a base Redis image
FROM redis:latest

# Copy your Redis configuration file into the container
COPY src/lib/redis/redis.conf /etc/redis/redis.conf

# Expose the Redis port (adjust as needed)
EXPOSE 6379

# Start Redis server with custom config
CMD ["redis-server", "/etc/redis/redis.conf"]
