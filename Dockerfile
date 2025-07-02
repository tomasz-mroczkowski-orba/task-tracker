# Use official Python image
FROM python:3.13.5-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (change if needed)
EXPOSE 8000

# Run the application (adjust if your entry point is different)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]