import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from langchain.tools import tool
load_dotenv()

firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

@tool
def blog_scraper(url:str) -> str:
    """Scrape a blog's URL and return the content"""

    scrape = firecrawl.scrape(url,formats= ["markdown"])
    return scrape.markdown if scrape.markdown else "No content found at the provided URL."





