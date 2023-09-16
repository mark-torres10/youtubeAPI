# Use Python 3.9
FROM python:3.9

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (if needed)
# RUN apt-get update && apt-get install -y ...

# Copy the entire project directory into the container
COPY . /app

# Set the working directory to the Django project
WORKDIR /app/src/backend

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Django server port (adjust as needed)
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
