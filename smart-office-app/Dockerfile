# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# 1. Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the rest of the application code
COPY . .

# 3. Create a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 4. Expose port 5000
EXPOSE 5000

# 5. Command to run the application
# We use "python run.py" instead of gunicorn to ensure the 
# database seeding logic (if __name__ == "__main__") is executed.
CMD ["python", "run.py"]