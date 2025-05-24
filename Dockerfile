# Use Python 3.11.9 as the base image
FROM python:3.11.9-slim

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-dev \
    libaio1 \
    default-libmysqlclient-dev \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Return to app directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .

RUN pip install mysqlclient>=2.2.0

# Install basic dependencies first
RUN pip install setuptools wheel pip --upgrade

# Install Flask and its dependencies first
RUN pip install Flask>=2.0.0 \
    Flask-SQLAlchemy>=2.5.1 \
    Flask-Migrate>=3.1.0 \
    Flask-Cors>=3.0.10

# Install Cython and other critical dependencies
RUN pip install Cython cryptography greenlet

# Install the rest of the requirements
RUN pip install -r requirements.txt

# Ensure gunicorn is installed
RUN pip install gunicorn>=20.1.0

# Copy project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Set environment variables for the application
ENV APP_NAME=Chartnalyze \
    APP_URL=http://localhost:8000 \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    UPLOAD_FOLDER=public \
    LIMITER_DEFAULT_LIMITS="3600 per hour" \
    OTP_EXPIRATION_MINUTES=30 \
    JWT_EXPIRATION_DAYS=30 \
    API_KEY=dev_api_key \
    SECRET_KEY=dev_secret_key \
    JWT_SECRET_KEY=dev_secret_key \
    SQLALCHEMY_TRACK_MODIFICATIONS=False \
    SQLALCHEMY_DATABASE_URI=sqlite:///chartnalyze.db \
    SQLALCHEMY_EXPIRE_ON_COMMIT=False \
    MONGO_URI=mongodb://localhost:27017/chartnalyze \
    MAIL_SERVER=sandbox.smtp.mailtrap.io \
    MAIL_PORT=2525 \
    MAIL_USERNAME=test \
    MAIL_PASSWORD=test \
    MAIL_USE_TLS=True \
    MAIL_USE_SSL=False \
    MAIL_DEFAULT_SENDER=chartnalyze@chartnalyze.edu

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]

