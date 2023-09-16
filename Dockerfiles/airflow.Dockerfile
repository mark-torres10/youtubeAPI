# Use Python 3.9
FROM python:3.9

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python packages from requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy your DAG file into the container
COPY src/dags/pipeline.py /app/dags/

# Expose the Airflow web UI port
EXPOSE 8080

# Start Airflow webserver
CMD ["airflow", "webserver"]
