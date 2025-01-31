from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

app = FastAPI(title="Browser Search API")

class SearchResult(BaseModel):
    title: str
    url: str | None = None
    snippet: str | None = None

class SearchRequest(BaseModel):
    query: str
    search_engine: str = "bing"  # default to bing

class SearchResponse(BaseModel):
    results: list[SearchResult]
    status_code: int
    execution_time: float
    search_engine: str

def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')  # For newer Chrome versions
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # Add random user agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=options)

def get_search_url(query: str, engine: str) -> str:
    if engine.lower() == "google":
        return f"https://www.google.com/search?q={query}"
    elif engine.lower() == "bing":
        return f"https://www.bing.com/search?q={query}"
    else:
        raise ValueError(f"Unsupported search engine: {engine}")

def parse_bing_results(html_content: str) -> list[SearchResult]:
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    
    # Find all search result elements
    for element in soup.select('#b_results .b_algo'):
        title_elem = element.find('h2')
        if not title_elem:
            continue
            
        title = title_elem.get_text(strip=True)
        url = title_elem.find('a')['href'] if title_elem.find('a') else None
        snippet = element.find(class_='b_caption').get_text(strip=True) if element.find(class_='b_caption') else None
        
        results.append(SearchResult(
            title=title,
            url=url,
            snippet=snippet
        ))
    
    return results[:10]  # Return top 10 results

def parse_google_results(html_content: str) -> list[SearchResult]:
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    
    # Find all search result elements
    for element in soup.select('div.g'):
        title_elem = element.select_one('h3')
        if not title_elem:
            continue
            
        title = title_elem.get_text(strip=True)
        url = element.find('a')['href'] if element.find('a') else None
        snippet = element.select_one('.VwiC3b').get_text(strip=True) if element.select_one('.VwiC3b') else None
        
        results.append(SearchResult(
            title=title,
            url=url,
            snippet=snippet
        ))
    
    return results[:10]  # Return top 10 results

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    start_time = time.time()
    
    try:
        driver = get_chrome_driver()
        search_url = get_search_url(request.query, request.search_engine)
        
        driver.get(search_url)
        html_content = driver.page_source
        status_code = 200
        
        # Parse results based on search engine
        if request.search_engine.lower() == "google":
            results = parse_google_results(html_content)
        else:
            results = parse_bing_results(html_content)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if 'driver' in locals():
            driver.quit()
    
    execution_time = time.time() - start_time
    
    return SearchResponse(
        results=results,
        status_code=status_code,
        execution_time=execution_time,
        search_engine=request.search_engine
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
