[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/uzaysozen-imdb-mcp-server-badge.png)](https://mseep.ai/app/uzaysozen-imdb-mcp-server)
# IMDb MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Available-blue.svg)](https://www.docker.com/)
[![RapidAPI](https://img.shields.io/badge/RapidAPI-IMDb-orange.svg)](https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236)
[![smithery badge](https://smithery.ai/badge/@uzaysozen/imdb-mcp-server)](https://smithery.ai/server/@uzaysozen/imdb-mcp-server)

[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/8ed9e57d-d9e7-4a5d-ab94-4113be3ee842)

[Verified on MCP Review](https://mcpreview.com/mcp-servers/uzaysozen/imdb-mcp-server)

A Python server implementing Model Context Protocol (MCP) for movie and TV show information using the IMDb API service.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Configuration](#configuration)
- [Tools](#tools)
  - [Search Tools](#search-tools)
  - [IMDb ID Tools](#imdb-id-tools)
  - [Configuration Tools](#configuration-tools)
  - [Movies Tools](#movies-tools)
  - [TV Shows Tools](#tv-shows-tools)
  - [Upcoming Releases Tools](#upcoming-releases-tools)
  - [India Spotlight Tools](#india-spotlight-tools)
- [Example Prompt and Response](#example-prompt-and-response)
- [Installation](#installation)
- [Starting the Server](#starting-the-server)
- [Technical Details](#technical-details)
  - [Pagination System](#pagination-system)
  - [Caching System](#caching-system)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

This server provides a comprehensive set of tools for accessing IMDb data through the IMDb API. It serves as a bridge between agents and the IMDb database, offering detailed information about movies, TV shows, actors, directors, and more.

## Features

- 🎬 Movie and TV show search capabilities
- 📋 Detailed information about movies and TV shows
- 👨‍👩‍👧‍👦 Cast and crew information
- 🏆 Top-rated and popular content lists
- 💰 Box office data
- 🌍 Country-specific movie information (with special focus on Indian cinema)
- 🔜 Upcoming releases
- 🔄 Efficient response caching system

## Configuration

This server requires an API key from RapidAPI for the IMDb API service:

1. Create an account on [RapidAPI](https://rapidapi.com/)
2. Subscribe to the [IMDb API](https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236) on RapidAPI
3. Set the environment variable:
   ```
   RAPID_API_KEY_IMDB=your_api_key_here
   ```

## Tools

### Search Tools

| Tool | Description | Example |
|------|-------------|---------|
| **search_imdb** | Search for movies and TV shows with various filtering options | `search_imdb(primary_title="Inception")` |

### IMDb ID Tools

| Tool | Description | Example |
|------|-------------|---------|
| **get_imdb_details** | Retrieve detailed information about a movie or TV show | `get_imdb_details(imdb_id="tt1375666")` |
| **get_directors** | Retrieve the directors of a movie | `get_directors(imdb_id="tt1375666")` |
| **get_cast** | Retrieve the cast of a movie | `get_cast(imdb_id="tt1375666")` |
| **get_writers** | Retrieve the writers of a movie | `get_writers(imdb_id="tt1375666")` |

### Configuration Tools

| Tool | Description | Example |
|------|-------------|---------|
| **get_types** | Get all available content types | `get_types()` |
| **get_genres** | Get all available genres | `get_genres()` |
| **get_countries** | Get all available countries | `get_countries()` |
| **get_languages** | Get all available languages | `get_languages()` |

### Movies Tools
*Paginated (5 results per page)*

| Tool | Description | Example |
|------|-------------|---------|
| **get_top_250_movies** | Get the top 250 movies from IMDb | `get_top_250_movies()` |
| **get_top_box_office_us** | Get the US box office records | `get_top_box_office_us()` |
| **get_most_popular_movies** | Get the most popular movies | `get_most_popular_movies()` |

### TV Shows Tools
*Paginated (5 results per page)*

| Tool | Description | Example |
|------|-------------|---------|
| **get_top_250_tv_shows** | Get the top 250 TV shows from IMDb | `get_top_250_tv_shows()` |
| **get_most_popular_tv_shows** | Get the most popular TV shows | `get_most_popular_tv_shows()` |

### Upcoming Releases Tools
*Paginated (5 results per page)*

| Tool | Description | Example |
|------|-------------|---------|
| **get_upcoming_releases** | Get upcoming movie and TV show releases by country | `get_upcoming_releases(country_code="US", type="MOVIE")` |
| **get_available_country_codes_for_upcoming_releases** | Get available country codes for upcoming releases | `get_available_country_codes_for_upcoming_releases()` |

### India Spotlight Tools (Paginated)
*Paginated (5 results per page)*

| Tool | Description | Example |
|------|-------------|---------|
| **get_top_rated_malayalam_movies** | Get top 50 rated Malayalam movies | `get_top_rated_malayalam_movies()` |
| **get_upcoming_indian_movies** | Get most anticipated upcoming Indian movies | `get_upcoming_indian_movies()` |
| **get_trending_tamil_movies** | Get trending Tamil movies | `get_trending_tamil_movies()` |
| **get_trending_telugu_movies** | Get trending Telugu movies | `get_trending_telugu_movies()` |
| **get_top_rated_tamil_movies** | Get top 50 rated Tamil movies | `get_top_rated_tamil_movies()` |
| **get_top_rated_telugu_movies** | Get top 50 rated Telugu movies | `get_top_rated_telugu_movies()` |
| **get_top_rated_indian_movies** | Get top 250 rated Indian movies | `get_top_rated_indian_movies()` |

## Example Prompt and Response

**What are the 5 action movies that will be released in the nearest future?**

I'll find the upcoming action movies for you.

Called MCP tool ```get_upcoming_releases```

Now I'll look for the action movies from these upcoming releases:

Called MCP tool ```get_upcoming_releases```

Based on the search results, here are the 5 upcoming action movies that will be released in the nearest future:

1. **A Minecraft Movie** (April 4, 2025)
   - Genres: Action, Adventure, Comedy
   - Description: Four misfits are pulled through a portal into a cubic wonderland and embark on a quest with an expert crafter to get back home.

2. **Freaky Tales** (April 4, 2025)
   - Genres: Action, Adventure, Comedy
   - Description: Four interconnected stories set in 1987 Oakland, CA about the love of music, movies, people, places and memories.

3. **Wake Up** (April 4, 2025)
   - Genres: Action, Horror
   - Description: Young activists invade a furniture store to protest environmental issues but find themselves trapped with a hunting-obsessed night guard.

4. **Warfare** (April 11, 2025)
   - Genres: Action, Drama, War
   - Description: Based on ex-Navy Seal Ray Mendoza's real-life experiences during the Iraq War.

5. **The Amateur** (April 11, 2025)
   - Genres: Action, Thriller
   - Description: A CIA cryptographer blackmails his agency into training him to pursue terrorists who killed his wife.

## Installation

### Installing via Smithery

To install IMDb Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@uzaysozen/imdb-mcp-server):

```bash
npx -y @smithery/cli install @uzaysozen/imdb-mcp-server --client claude
```

### Option 1: Using Docker (Recommended)

1. Clone this repository
```bash
git clone https://github.com/uzaysozen/imdb-mcp-server.git
cd imdb-mcp-server
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Build the Docker image
```bash
docker build -t imdb_server .
```

4. Run the Docker container (ensure your API key is passed as an environment variable)
```bash
docker run -d -p 8000:8000 -e RAPID_API_KEY_IMDB=your_api_key_here --name imdb_server imdb_server
```

5. Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "imdb_server": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "imdb_server",
        "imdb-mcp-server"
      ],
      "env": {
        "RAPID_API_KEY_IMDB": "your_api_key_here"
      }
    }
  }
}
```

### Option 2: Direct Python Execution

1. Clone this repository
```bash
git clone https://github.com/uzaysozen/imdb-mcp-server.git
cd imdb-mcp-server
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set the API key environment variable
```bash
export RAPID_API_KEY_IMDB=your_api_key_here
```

4. Add this to your `claude_desktop_config.json`, adjusting the Python path as needed:

```json
{
  "mcpServers": {
    "imdb_server": {
      "command": "/path/to/your/python",
      "args": [
        "/path/to/imdb_server.py"
      ],
      "env": {
        "RAPID_API_KEY_IMDB": "your_api_key_here"
      }
    }
  }
}
```

## Starting the Server

```bash
# Start the server directly
python imdb_server.py

# Or using MCP CLI
mcp run imdb_server.py

# Or if using Docker, the server starts automatically with the container
docker run -d -p 8000:8000 -e RAPID_API_KEY_IMDB=your_api_key_here --name imdb_server imdb_server
```

After adding your chosen configuration, restart Claude Desktop to load the IMDb server. You'll then be able to use all the movie and TV show data tools in your conversations with Claude.

## Technical Details

The server is built on:
- IMDb API via RapidAPI
- MCP for API interface
- Requests for API communication
- FastMCP for server implementation
- Custom in-memory caching system
- Smart pagination that limits results to 5 items per request, optimizing for AI agent consumption

### Pagination System

All data retrieval tools implement pagination to enhance AI agent performance:

#### Purpose
- **AI-Optimized Responses**: Limits each response to 5 items, preventing overwhelm in AI agents that process the data
- **Focused Results**: Helps agents provide more relevant and concise information to users
- **Improved Processing**: Reduces the cognitive load on AI agents when analyzing movie and TV show data

#### Implementation
- Each paginated endpoint accepts a `start` parameter (default: 0)
- Results include navigation metadata (totalCount, hasMore, nextStart)
- Consistent 5-item page size across all collection endpoints
- Example request with pagination: `get_top_250_movies(start=5)` returns items 6-10

#### Benefits
- **Better Agent Responses**: Prevents AI agents from receiving too much data at once
- **Manageable Information**: Creates digestible chunks of data that agents can process effectively
- **Sequential Access**: Allows structured exploration of large datasets through multiple tool calls

### Caching System

The server implements an efficient caching system to improve performance and reduce API calls:

#### Features

- **In-memory Cache**: Stores API responses in memory for quick retrieval
- **Configurable Expiration and Size**: Cache entries expire after a customizable time period (default: 10 minutes) and have a default size of 100 cache keys
- **Automatic Cache Cleaning**: Periodically (default: 5 minutes) removes expired entries to manage memory usage using a background thread
- **Cache Keys**: Generated based on the URL and query parameters to ensure uniqueness

#### Benefits

- **Reduced API Usage**: Helps stay within API rate limits by reusing responses
- **Faster Response Times**: Eliminates network latency for cached queries
- **Cost Efficiency**: Minimizes the number of API calls, especially for popular or repeated queries

#### Configuration

The cache size and expiration time can be adjusted in the code:

```python
# Default are 600 seconds (10 minutes) and 100 cache keys
response_cache = ResponseCache(expiry_seconds=120, max_size=50)
```

## Limitations

- API rate limits apply based on your RapidAPI subscription
- Some detailed information may require additional API calls
- Search results may be limited to a certain number of items per request
- In-memory cache is lost when server restarts
- All paginated responses return a maximum of 5 items per page

## Troubleshooting

| Problem | Solution |
|---------|----------|
| API key not recognized | Ensure the RAPID_API_KEY_IMDB environment variable is properly set |
| Rate limit exceeded | Check your RapidAPI subscription tier and limits |
| Timeout errors | The server has a 30-second timeout; for large requests, try limiting parameters |
| Empty results | Try broader search terms or check if the content exists in IMDb's database |
| High memory usage | If running for extended periods with many unique queries, restart the server occasionally to clear the cache |

## License

This MCP server is available under the MIT License.
