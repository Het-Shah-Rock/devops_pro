# ==========================================
# DEV: MULTI-STAGE DOCKERFILE
# ==========================================
# Stage 1: Build Dependencies
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final Runtime Environment
FROM python:3.10-slim

WORKDIR /app

# Add a non-root user for security (Industry Standard)
RUN useradd -m appuser
USER appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source code
COPY . .

# Ensure local bin is on PATH for Streamlit
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
