# GIIA - Lápiz Inteligente API

API REST para recibir datos de un lápiz digital mediante MQTT y almacenarlos en MySQL para análisis posterior.

> Proyecto en desarrollo.

---

## Arquitectura

```txt
Lápiz Digital → MQTT → Backend API → MySQL
```

---

## Requisitos

Solo necesitas Docker y Docker Compose.

No es necesario instalar:

* Python
* MySQL
* Mosquitto

Todo corre dentro de contenedores.

---

## Inicio rápido

```bash
git clone <url-del-repo>
cd GIIA_lapiz_inteligente

cp .env.example .env

docker compose up -d
```

Verificar que la API esté funcionando:

```bash
curl http://localhost:8001/health
```

---

## Accesos

* API Docs (Swagger): [http://localhost:8001/docs](http://localhost:8001/docs)
* Redoc: [http://localhost:8001/redoc](http://localhost:8001/redoc)

---

## Servicios

| Servicio    | Puerto | Descripción          |
| ----------- | ------ | -------------------- |
| Backend API | 8001   | API REST con FastAPI |
| MySQL       | 3306   | Base de datos        |
| Mosquitto   | 1883   | Broker MQTT          |

---

## Comandos útiles

| Acción                  | Comando                                |
| ----------------------- | -------------------------------------- |
| Ver logs del backend    | `docker compose logs -f backend`       |
| Reconstruir backend     | `docker compose up -d --build backend` |
| Detener servicios       | `docker compose down`                  |
| Detener y borrar BD     | `docker compose down -v`               |
| Ver estado de servicios | `docker compose ps`                    |
| Abrir shell del backend | `docker compose exec backend bash`     |

---

## Desarrollo

Los cambios dentro de `backend/` se recargan automáticamente mediante hot-reload.

Si agregas nuevas dependencias en `requirements.txt`, reconstruye el contenedor:

```bash
docker compose up -d --build backend
```

---

## Estructura del proyecto

```txt
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── auth/           # Autenticación
│       ├── core/           # Configuración y seguridad
│       ├── db/             # Conexión a MySQL
│       ├── children/       # Gestión de niños
│       ├── exercises/      # Ejercicios
│       ├── mqtt/           # Comunicación MQTT
│       └── sessions/       # Sesiones
│
├── mosquitto/
│   └── config/
│       └── mosquitto.conf
│
├── sql/
│   ├── init.sql
│   └── seed.sql
│
├── docker-compose.yml
└── .env.example
```

---

## Base de datos

Los scripts SQL dentro de `sql/` se ejecutan automáticamente al iniciar MySQL:

* `init.sql` → estructura de tablas
* `seed.sql` → datos iniciales

---

## Notas importantes

* Cada integrante debe crear su propio archivo `.env`.
* Usar nombres de servicio Docker (`mysql_server`, `mosquitto`) en lugar de `localhost`.
* Crear ramas desde `main`.
* Abrir Pull Requests antes de hacer merge.

---

## Problemas comunes

### El backend no inicia

Reconstruir el contenedor:

```bash
docker compose up -d --build backend
```

---

### Error de puertos ocupados

Verificar que los siguientes puertos no estén siendo utilizados:

* `8001`
* `3306`
* `1883`

---

## Estado actual

* Backend API
* Docker Compose
* MySQL
* MQTT Broker
* Autenticación base

Módulos en desarrollo:

* Children
* Exercises
* Sessions
* MQTT ingestion
