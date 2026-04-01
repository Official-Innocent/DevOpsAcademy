FROM python:3.11-slim
WORKDIR /app
ENV DEVELOPER_NAME="Innocent" \
    ENVIRONMENT="development" \
    APP_VERSION="1.0"
COPY app.py .
RUN pip install psutil --break-system-packages
EXPOSE 5000
CMD ["python3", "app.py"]
