FROM python:3.11-alpine

WORKDIR /chartnalyze

# Install system dependencies
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    build-base \
    python3-dev \
    mariadb-dev \
    gcc \
    musl-dev

COPY requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip 

# Install all Python dependencies
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Run the application on development mode
CMD [ "flask", "run" , "--debug", "--host=0.0.0.0", "--port=8000"]