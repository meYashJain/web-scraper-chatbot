import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def scrape_url(self, url):
        """Scrape content from a single URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted tags
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Extract main content
            text = soup.get_text(separator='\n', strip=True)
            return {
                'url': url,
                'content': text,
                'domain': urlparse(url).netloc
            }
            
        except Exception as e:
            print(f"Scraping failed: {str(e)}")
            return None