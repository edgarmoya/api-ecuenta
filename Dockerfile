# Usar una imagen base con Python
FROM python:3.11.7

# Instala OpenJDK 17
RUN apt update && apt install -y openjdk-17-jdk && rm -rf /var/lib/apt/lists/*

# Configurar JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./scripts /code/scripts

CMD ["bash", "-c", "python scripts/create_superuser.py && uvicorn app.main:app --host 0.0.0.0 --port 80 --proxy-headers"]