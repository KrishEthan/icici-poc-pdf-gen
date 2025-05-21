FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wkhtmltopdf \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Expose port if running a web server (optional)
EXPOSE 8002

CMD ["python", "main.py"]