FROM python:3.10-slim

WORKDIR /app

# Only copy requirements first
COPY requirements.txt .

# Install dependencies early and cache it
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the app
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]

