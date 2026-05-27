# Detalle Backend - Lapiz inteligente

## tree

``` bash
.
├── backend
│   ├── app
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   ├── model.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-311.pyc
│   │   │   │   ├── model.cpython-311.pyc
│   │   │   │   └── routes.cpython-311.pyc
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── children
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── config.cpython-311.pyc
│   │   │   │   └── __init__.cpython-311.pyc
│   │   │   └── security.py
│   │   ├── db
│   │   │   ├── base.py
│   │   │   ├── database.py
│   │   │   ├── __init__.py
│   │   │   └── __pycache__
│   │   │       ├── database.cpython-311.pyc
│   │   │       └── __init__.cpython-311.pyc
│   │   ├── dependencies
│   │   ├── exercises
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── mqtt
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   └── main.cpython-311.pyc
│   │   ├── sessions
│   │   └── websocket
│   ├── Dockerfile
│   └── requirements.txt
├── detalle_backend.md
├── docker-compose.yml
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── mosquitto
│   └── config
│       └── mosquitto.conf
├── README.md
└── sql
    ├── init.sql
    ├── procedures
    └── seed.sql
```

## .env

``` shell
MYSQL_HOST=mysql_server
MYSQL_PORT=3306
MYSQL_ROOT_PASSWORD=giia_root_password
MYSQL_USER=giia_user
MYSQL_PASSWORD=giia_password
MYSQL_DATABASE=GIIA_lapiz_inteligente

BACKEND_HOST=0.0.0.0
BACKEND_PORT=8001

JWT_SECRET_KEY=nwAvRL0yeqzVmSi8wl4Y
JWT_EXPIRATION=240
JWT_ALGORITHM=HS256

MQTT_BROKER=mosquitto
MQTT_PORT=1883
```

## ./docker-compose.yml

``` yml
services:
  mysql_server:
    image: mysql:8.0
    container_name: lapiz_mysql
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./sql/init.sql:/docker-entrypoint-initdb.d/01_init.sql
      - ./sql/seed.sql:/docker-entrypoint-initdb.d/02_seed.sql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - lapiz_network

  mosquitto:
    image: eclipse-mosquitto:2
    container_name: lapiz_mosquitto
    restart: unless-stopped
    volumes:
      - ./mosquitto/config/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - mosquitto_data:/mosquitto/data
      - mosquitto_logs:/mosquitto/log
    networks:
      - lapiz_network

  backend:
    build: ./backend
    container_name: lapiz_backend
    restart: unless-stopped
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "${BACKEND_PORT}:8000"
    env_file:
      - .env
    depends_on:
      mysql_server:
        condition: service_healthy
      mosquitto:
        condition: service_started
    volumes:
      - ./backend/app:/app
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    networks:
      - lapiz_network

volumes:
  mysql_data:
  mosquitto_data:
  mosquitto_logs:

networks:
  lapiz_network:
    driver: bridge
```

## ./backend/Dockerfile

``` dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

