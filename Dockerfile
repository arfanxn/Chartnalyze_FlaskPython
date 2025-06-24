FROM python:3.11-slim

WORKDIR /chartnalyze

RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb-dev \
    build-essential \
    pkg-config \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip

# Install all Python dependencies
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Run the application on development mode
CMD [ "flask", "run" , "--debug", "--host=0.0.0.0", "--port=8000"]