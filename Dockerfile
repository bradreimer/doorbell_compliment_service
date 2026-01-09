# Base image from Jetson PyTorch wheels
FROM dustynv/l4t-pytorch:r36.4.0

# Set working directory
WORKDIR /workspace/doorbell_compliment_service

# Copy only your application code
COPY app/ ./app/
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
