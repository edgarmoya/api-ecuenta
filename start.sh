#!/bin/bash
# Instalar Java
apt-get update && apt-get install -y openjdk-11-jre

# Ejecutar FastAPI
uvicorn main:app --host 0.0.0.0 --port $PORT
