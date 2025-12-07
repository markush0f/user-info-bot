# User Info Bot – Local Installation Guide

Este proyecto es un chatbot avanzado capaz de responder con **información real del usuario**, combinando scraping web mediante **HeadlessX**, análisis de repositorios de GitHub, bases vectoriales y arquitectura RAG utilizando la API de OpenAI.

A continuación se explica cómo ejecutarlo **en local**, incluyendo base de datos con Docker y configuración completa mediante variables de entorno.

---

## 1. Requirements

* Python 3.11+
* Docker y Docker Compose
* Git
* Una API Key de OpenAI

---

## 2. Clone the Repository

```bash
git clone https://github.com/markush0f/user-info-bot.git
cd user-info-bot
```

---

## 3. Environment Variables

Antes de continuar, es necesario descargar e instalar el proyecto **HeadlessX**, ya que es un requisito para el scraping avanzado utilizado por este bot.

📌 **Repositorio y documentación de HeadlessX:**
[https://headlessx.saify.me/#api](https://headlessx.saify.me/#api)

Sigue sus instrucciones para levantar el servicio o generar tus claves de acceso.

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# OPENAI
OPENAI_API_KEY=

# DATABASE
USER_DB=
PASSWORD_DB=
DATABASE=
HOST=
PORT=
# REQUIRED if you use PSYCOPG2,
# SSL=require

# GITHUB
GITHUB_TOKEN=

# HEADLESSX
# Or use: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
HEADLESSX_AUTH_TOKEN=
HEADLESSX_API=
```

---

## 4. Start the Database with Docker

Ejecuta el servicio de PostgreSQL usando Docker Compose:

```bash
docker compose up -d
```

---

## 5. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 6. Run the Backend

Inicia el servidor FastAPI:

```bash
uvicorn app.main:app --reload
```

El proyecto estará disponible en:

```
http://localhost:8000
```

Documentación interactiva:

```
http://localhost:8000/docs
```

---

## 7. Summary

Con esta guía podrás ejecutar el proyecto localmente con:

* PostgreSQL vía Docker
* Backend FastAPI configurado
* Variables de entorno listas para producción/desarrollo

Si deseas que añada instrucciones para despliegue en VPS o Dockerizar completamente el backend, puedo extender este README.
