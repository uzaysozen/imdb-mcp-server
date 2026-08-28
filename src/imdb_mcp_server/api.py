import os
from typing import Any, Dict, Optional

import requests
from mcp.server.mcpserver.exceptions import ToolError

from .cache import cache_manager


# Constants
BASE_URL = "https://imdb236.p.rapidapi.com/api/imdb"
RAPIDAPI_HOST = "imdb236.p.rapidapi.com"
SUBSCRIBE_URL = "https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236"


async def make_imdb_request(
    url: str, querystring: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """Make a request to the IMDb API with caching and helpful error messages.

    The API key is read from the ``RAPID_API_KEY_IMDB`` environment variable.
    """
    querystring = querystring or {}

    # Check if it's time to clean the cache
    cache_manager.cleanup_if_needed()

    # Create a cache key from the URL and querystring
    cache_key = f"{url}_{querystring}"

    # Try to get from cache first
    cached_data = cache_manager.cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    api_key = os.getenv("RAPID_API_KEY_IMDB")
    if not api_key:
        raise ToolError(
            "API key not found. Set the RAPID_API_KEY_IMDB environment variable "
            f"(subscribe to the IMDb API at {SUBSCRIBE_URL})."
        )

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30.0)
        response.raise_for_status()
        data = response.json()

        # Cache the response
        cache_manager.cache.set(cache_key, data)

        return data
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status in (401, 403):
            raise ToolError(
                f"IMDb API rejected the request (HTTP {status}). Your RapidAPI key is "
                "missing, invalid, or not subscribed to the IMDb API. Subscribe at "
                f"{SUBSCRIBE_URL} and set RAPID_API_KEY_IMDB."
            )
        if status == 404:
            raise ToolError(
                "IMDb API returned HTTP 404. The endpoint may have changed or your "
                f"RapidAPI subscription to the IMDb API is inactive. Check it at {SUBSCRIBE_URL}."
            )
        if status == 429:
            raise ToolError(
                "IMDb API rate limit exceeded (HTTP 429). Check your RapidAPI plan limits."
            )
        raise ToolError(f"Unable to fetch data from IMDb. Please try again later. Error: {e}")
    except Exception as e:
        raise ToolError(f"Unable to fetch data from IMDb. Please try again later. Error: {e}")


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
        "nextStart": end if end < total_count else None,
    }
