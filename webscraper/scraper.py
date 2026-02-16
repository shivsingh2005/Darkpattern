"""
Core web scraping functionality.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """
    A web scraper class for fetching and parsing website content.
    """
    
    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = 30):
        """
        Initialize the WebScraper.
        
        Args:
            headers: Optional custom headers for HTTP requests
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch(self, url: str) -> Optional[str]:
        """
        Fetch the content of a URL.
        
        Args:
            url: The URL to fetch
            
        Returns:
            HTML content as string, or None if request fails
        """
        try:
            logger.info(f"Fetching URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Successfully fetched {url}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse(self, html: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html: HTML content as string
            
        Returns:
            BeautifulSoup object, or None if parsing fails
        """
        try:
            return BeautifulSoup(html, 'lxml')
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None
    
    def get_text_content(self, url: str) -> Optional[str]:
        """
        Get all text content from a URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Text content as string, or None if failed
        """
        html = self.fetch(url)
        if html is None:
            return None
        
        soup = self.parse(html)
        if soup is None:
            return None
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def get_links(self, url: str) -> List[str]:
        """
        Get all links from a URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            List of URLs
        """
        html = self.fetch(url)
        if html is None:
            return []
        
        soup = self.parse(html)
        if soup is None:
            return []
        
        links = []
        for link in soup.find_all('a', href=True):
            links.append(link['href'])
        
        return links
    
    def get_images(self, url: str) -> List[str]:
        """
        Get all image URLs from a URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            List of image URLs
        """
        html = self.fetch(url)
        if html is None:
            return []
        
        soup = self.parse(html)
        if soup is None:
            return []
        
        images = []
        for img in soup.find_all('img', src=True):
            images.append(img['src'])
        
        return images
    
    def get_elements(self, url: str, selector: str) -> List[str]:
        """
        Get elements matching a CSS selector.
        
        Args:
            url: The URL to scrape
            selector: CSS selector
            
        Returns:
            List of element texts
        """
        html = self.fetch(url)
        if html is None:
            return []
        
        soup = self.parse(html)
        if soup is None:
            return []
        
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]
    
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape a URL and return all available data.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing scraped data
        """
        result = {
            'url': url,
            'success': False,
            'text_content': None,
            'links': [],
            'images': [],
            'error': None
        }
        
        html = self.fetch(url)
        if html is None:
            result['error'] = 'Failed to fetch URL'
            return result
        
        soup = self.parse(html)
        if soup is None:
            result['error'] = 'Failed to parse HTML'
            return result
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        result['text_content'] = ' '.join(chunk for chunk in chunks if chunk)
        
        # Get links
        for link in soup.find_all('a', href=True):
            result['links'].append(link['href'])
        
        # Get images
        for img in soup.find_all('img', src=True):
            result['images'].append(img['src'])
        
        result['success'] = True
        return result


# Convenience functions
def scrape_url(url: str) -> Dict[str, Any]:
    """
    Convenience function to scrape a URL.
    
    Args:
        url: The URL to scrape
        
    Returns:
        Dictionary containing scraped data
    """
    scraper = WebScraper()
    return scraper.scrape(url)


def get_text_content(url: str) -> Optional[str]:
    """
    Convenience function to get text content from a URL.
    
    Args:
        url: The URL to scrape
        
    Returns:
        Text content as string, or None if failed
    """
    scraper = WebScraper()
    return scraper.get_text_content(url)
