# Browser Search API

A FastAPI-based service that performs browser searches using headless Chrome and returns raw HTML results.

## Features

- Headless Chrome browser integration using Selenium
- Search query support for multiple search engines (Google, Bing)
- Docker containerization
- Response includes HTML content, status code, and execution time

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn app:app --reload
```

## Running with Docker

1. Build the container:
```bash
docker build -t browser-search .
```

2. Run the container:
```bash
docker run -p 8000:8000 browser-search
```

## API Usage

### Search Endpoint

```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "your search query", "search_engine": "google"}'
```

### Health Check

```bash
curl "http://localhost:8000/health"
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
