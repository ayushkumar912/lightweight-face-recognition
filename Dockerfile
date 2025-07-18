# Multi-stage build for optimized face recognition system
FROM python:3.11-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libopenblas0 \
    liblapack3 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1-mesa-glx \
    libgtk-3-0 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Create necessary directories
RUN mkdir -p /app/backend/known_faces \
    /app/backend/resorces \
    /app/api \
    /app/frontend/static \
    /app/frontend/templates \
    && chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Download dlib models if not present
RUN if [ ! -f backend/resorces/shape_predictor_68_face_landmarks.dat ]; then \
        wget -O backend/resorces/shape_predictor_68_face_landmarks.dat \
        https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2 && \
        cd backend/resorces && bunzip2 shape_predictor_68_face_landmarks.dat.bz2; \
    fi

RUN if [ ! -f backend/resorces/dlib_face_recognition_resnet_model_v1.dat ]; then \
        wget -O backend/resorces/dlib_face_recognition_resnet_model_v1.dat \
        https://github.com/davisking/dlib-models/raw/master/dlib_face_recognition_resnet_model_v1.dat.bz2 && \
        cd backend/resorces && bunzip2 dlib_face_recognition_resnet_model_v1.dat.bz2; \
    fi

# Switch to non-root user
USER appuser

# Make sure the Python packages are in PATH
ENV PATH="/home/appuser/.local/bin:$PATH"
ENV PYTHONPATH="/app/backend:$PYTHONPATH"
ENV FLASK_HOST="0.0.0.0"
ENV FLASK_PORT="5000"
ENV FLASK_ENV="production"

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start the application
CMD ["python", "api/app.py"]
