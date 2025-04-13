# Cerus v0.1

A FastAPI-based LLM recommendation engine using LangChain, FAISS, Google LLM, and React-based admin UI.

## Features

- RAG-based inference using LangChain
- Per-client prompt templates
- Vector indexing of PDFs/text
- Admin UI to upload prompt templates
- FastAPI backend with Swagger
- Dockerized for prod

## Run Locally

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker-compose up --build
```
