import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from langchain.tools import tool
load_dotenv()

firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

@tool
def blog_scraper(url):
    """Scrape a blog's URL and return the content"""
    
    scrape = firecrawl.scrape_url("https://example.com/blog-post",params={"formats": ["markdown"]})
    return scrape.get('markdown','')


