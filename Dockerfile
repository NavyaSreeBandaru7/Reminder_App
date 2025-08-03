FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory
RUN mkdir -p data static/voice_notes

# Set permissions
RUN chmod -R a+rwx /app

EXPOSE 8501

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8501"]
