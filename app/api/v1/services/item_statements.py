from urllib.error import HTTPError
from cachetools import TTLCache     # FOR SMALL DEPLOYMENT ONLY. REMOVE WHEN SCALING TO MULTIPLE INSTANCE.
import httpx
import os

from app.api.v1.utils import scraping

cache = TTLCache(maxsize=10, ttl=300)  # 10 items, 5 min expiry

async def fetch_text(url: str, attach_url: str) -> str:
    headers = {     # mimics user request
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=False) as client:
        resp = await client.get(url)
        redirect_url = resp.headers["location"]  # shows the new URL it's redirecting to

        resp = await client.get(redirect_url+attach_url)
        if resp.status_code != 200:
            raise HTTPError(resp.url, resp.status_code, "", resp.headers, None) # For dev purpose.

    return resp.text


async def get_item(ticker: str, type_statement: str) -> dict:
    cache_key = f"{ticker}-{type_statement}"

    if cache_key in cache:
        return cache[cache_key]  

    try:
        # Fetch the item.
        url = os.getenv(type_statement) 
        html_text = await fetch_text(url.format(ticker), type_statement.replace('_','-').lower())
        
        # Build the item.
        raw_data = scraping.scrape_statement(html_text)
        statement = scraping.fixed_data(raw_data)
    except HTTPError as err:
        raise ValueError(f"The ticker does not exist from the source material")
    except KeyError as err:
        raise ValueError(f"The ticker does not have data from the source material")
    
    cache[cache_key] = statement

    return statement
