import json
import os
from typing import Any, Dict, Optional
import requests
from mcp.server.fastmcp import Context

from .cache import cache_manager


# Constants
BASE_URL = "https://imdb236.p.rapidapi.com/api/imdb"


async def make_imdb_request(url: str, querystring: dict[str, Any], ctx: Optional[Context] = None) -> Optional[Dict[str, Any]]:
    """Make a request to the IMDb API with proper error handling and caching."""
    
    # Check if it's time to clean the cache
    cache_manager.cleanup_if_needed()
    
    # Create a cache key from the URL and querystring
    cache_key = f"{url}_{str(querystring)}"
    
    # Try to get from cache first
    cached_data = cache_manager.cache.get(cache_key)
    if cached_data:
        return cached_data
    
    # Get API key from session config or fallback to environment variable
    api_key = None
    if ctx and hasattr(ctx, 'session_config') and ctx.session_config:
        api_key = ctx.session_config.rapidApiKeyImdb
    
    if not api_key:
        api_key = os.getenv("RAPID_API_KEY_IMDB")
    
    # Not in cache, make the request
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "imdb236.p.rapidapi.com",
    }
    
    if not api_key:
        raise ValueError("API key not found. Please set the RAPID_API_KEY_IMDB environment variable or provide rapidApiKeyImdb in the request.")
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        
        # Cache the response
        cache_manager.cache.set(cache_key, data)
            
        return data
    except Exception as e:
        raise ValueError(f"Unable to fetch data from IMDb. Please try again later. Error: {e}")


def paginated_response(items, start, total_count=None):
    """Format a paginated response with a fixed page size of 5."""
    if total_count is None:
        total_count = len(items)
    
    # Validate starting index
    start = max(0, min(total_count - 1 if total_count > 0 else 0, start))
    
    # Fixed page size of 5
    page_size = 5
    end = min(start + page_size, total_count)
    
    return {
        "items": items[start:end],
        "start": start,
        "count": end - start,
        "totalCount": total_count,
        "hasMore": end < total_count,
        "nextStart": end if end < total_count else None
    }
