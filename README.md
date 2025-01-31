# Browser Search API

A FastAPI-based service that performs browser searches using headless Chrome and returns raw HTML results from multiple search engines.

## Features

- Multi-engine support:
  - Google
  - Bing (default)
  - Yahoo
  - DuckDuckGo
- Headless Chrome browser integration using Selenium
- Clean, structured JSON responses
- Docker containerization
- Response includes search results, status code, and execution time

## Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Chrome/Chromium browser (for local development)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd browser-search
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

1. Build the container:
```bash
docker build -t browser-search .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 browser-search
```

## API Usage

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Search
```http
POST /search
```

Request body:
```json
{
  "query": "your search query",
  "search_engine": "bing"  // Optional, defaults to "bing"
}
```

Supported search engines:
- `"google"`: Google Search
- `"bing"`: Bing Search (default)
- `"yahoo"`: Yahoo Search
- `"duckduckgo"`: DuckDuckGo Search

Example response:
```json
{
  "results": [
    {
      "title": "Result title",
      "url": "Result URL",
      "snippet": "Result description"
    }
  ],
  "status_code": 200,
  "execution_time": 1.234,
  "search_engine": "bing"
}
```

#### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

### Example Usage

1. Basic search (using default Bing engine):
```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "python programming"}'
```

2. Search using Google:
```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "python programming", "search_engine": "google"}'
```

3. Search using Yahoo:
```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "python programming", "search_engine": "yahoo"}'
```

4. Search using DuckDuckGo:
```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "python programming", "search_engine": "duckduckgo"}'
```

## API Documentation

Once the server is running, you can access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

The project structure is organized as follows:
```
browser-search/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── .dockerignore     # Docker ignore rules
├── .gitignore        # Git ignore rules
└── README.md         # Documentation
```

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Successful search
- 400: Invalid request (e.g., unsupported search engine)
- 500: Server error (e.g., search engine unavailable)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
