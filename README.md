[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/uzaysozen-imdb-mcp-server-badge.png)](https://mseep.ai/app/uzaysozen-imdb-mcp-server)
# IMDb MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Available-blue.svg)](https://www.docker.com/)
[![RapidAPI](https://img.shields.io/badge/RapidAPI-IMDb-orange.svg)](https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236)

[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/8ed9e57d-d9e7-4a5d-ab94-4113be3ee842)

[Verified on MCP Review](https://mcpreview.com/mcp-servers/uzaysozen/imdb-mcp-server)

A Python server implementing Model Context Protocol (MCP) for movie and TV show information using the IMDb API service.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
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
  - [Transport Modes](#transport-modes)
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

## Requirements

- **Python**: 3.13 or higher
- **Package Manager**: uv (recommended) or pip
- **RapidAPI Account**: Required for IMDb API access

## Configuration

This server requires your own API key from RapidAPI for the IMDb API service:

1. Create an account on [RapidAPI](https://rapidapi.com/)
2. Subscribe to the [IMDb API](https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236) on RapidAPI (a free tier is available)
3. Copy your API key from the RapidAPI dashboard
4. Provide it via the `RAPID_API_KEY_IMDB` environment variable, using whichever fits your setup:
   - **MCP client config** — set it in the `env` block (see [Installation](#installation)). This is the usual way.
   - **Shell**: `export RAPID_API_KEY_IMDB=your_api_key_here`
   - **`.env` file**: copy `.env.example` to `.env`, then run with `uv run --env-file .env imdb-server`
   - **HTTP / Docker**: pass `-e RAPID_API_KEY_IMDB=...` to the container

The key is only needed when a tool is actually called — the server starts and lists its tools without it.

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
| **get_top_250_movies** | Get the top 250 movies from IMDb | `get_top_250_movies(start=0)` |
| **get_top_box_office_us** | Get the US box office records | `get_top_box_office_us(start=0)` |
| **get_most_popular_movies** | Get the most popular movies | `get_most_popular_movies(start=0)` |

### TV Shows Tools
*Paginated (5 results per page)*

| Tool | Description | Example |
|------|-------------|---------|
| **get_top_250_tv_shows** | Get the top 250 TV shows from IMDb | `get_top_250_tv_shows(start=0)` |
| **get_most_popular_tv_shows** | Get the most popular TV shows | `get_most_popular_tv_shows(start=0)` |

### Upcoming Releases Tools
*Paginated (5 results per page)*

| Tool | Description | Example |
|------|-------------|---------|
| **get_upcoming_releases** | Get upcoming movie and TV show releases by country | `get_upcoming_releases(country_code="US", type="MOVIE", start=0)` |
| **get_country_codes_for_upcoming_releases** | Get available country codes for upcoming releases | `get_country_codes_for_upcoming_releases()` |

### India Spotlight Tools
*Paginated (5 results per page)*

| Tool | Description | Example |
|------|-------------|---------|
| **get_top_rated_malayalam_movies** | Get top 50 rated Malayalam movies | `get_top_rated_malayalam_movies(start=0)` |
| **get_upcoming_indian_movies** | Get most anticipated upcoming Indian movies | `get_upcoming_indian_movies(start=0)` |
| **get_trending_tamil_movies** | Get trending Tamil movies | `get_trending_tamil_movies(start=0)` |
| **get_trending_telugu_movies** | Get trending Telugu movies | `get_trending_telugu_movies(start=0)` |
| **get_top_rated_tamil_movies** | Get top 50 rated Tamil movies | `get_top_rated_tamil_movies(start=0)` |
| **get_top_rated_telugu_movies** | Get top 50 rated Telugu movies | `get_top_rated_telugu_movies(start=0)` |
| **get_top_rated_indian_movies** | Get top 250 rated Indian movies | `get_top_rated_indian_movies(start=0)` |

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

This is a self-contained MCP server that you run locally with your own RapidAPI key.
Smithery no longer provides free managed hosting, so there is no shared remote
instance — clone (or `uvx`) the server and point your MCP client at it.

### Option 1: Run with uvx (no clone required)

If you have [uv](https://docs.astral.sh/uv/) installed, add this to your MCP client
config (e.g. `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "imdb_server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/uzaysozen/imdb-mcp-server",
        "imdb-server"
      ],
      "env": {
        "RAPID_API_KEY_IMDB": "your_api_key_here"
      }
    }
  }
}
```

### Option 2: Clone and run with uv

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/):
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Clone this repository and install dependencies:
```bash
git clone https://github.com/uzaysozen/imdb-mcp-server.git
cd imdb-mcp-server
uv sync
```

3. Add this to your MCP client config:
```json
{
  "mcpServers": {
    "imdb_server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/imdb-mcp-server",
        "run",
        "imdb-server"
      ],
      "env": {
        "RAPID_API_KEY_IMDB": "your_api_key_here"
      }
    }
  }
}
```

### Option 3: Self-host over HTTP (Docker)

For a shared, always-on remote server, run it in HTTP mode behind your own HTTPS
endpoint. This is optional and only needed if multiple clients should reach one
instance.

1. Clone this repository
```bash
git clone https://github.com/uzaysozen/imdb-mcp-server.git
cd imdb-mcp-server
```

2. Build and run the Docker image
```bash
docker build -t imdb_server .
docker run -d -p 8081:8081 -e RAPID_API_KEY_IMDB=your_api_key_here --name imdb_server imdb_server
```

The container runs in HTTP mode on port 8081, serving the MCP endpoint at `/mcp`.
Put it behind a reverse proxy / platform that terminates TLS. If you want it listed
on Smithery, register your public `https://.../mcp` URL as an external server at
[smithery.ai/new](https://smithery.ai/new).

## Starting the Server

### Stdio Mode (Default for local development)
```bash
# Using uv (recommended)
uv run imdb-server

# Or directly with Python module
python -m imdb_mcp_server
```

### HTTP Mode (for self-hosting)
```bash
# Using uv
TRANSPORT=http uv run imdb-server

# Or with Python module
TRANSPORT=http python -m imdb_mcp_server

# With custom port
TRANSPORT=http PORT=8081 uv run imdb-server
```

After adding your chosen configuration, restart your MCP client (e.g. Claude Desktop) to load the IMDb server. You'll then be able to use all the movie and TV show data tools in your conversations.

## Technical Details

The server is built on:
- **Python 3.13+**: Modern Python runtime
- **MCP Python SDK 2.x** (`mcp.server.mcpserver.MCPServer`): stdio and Streamable HTTP transports
- **IMDb API via RapidAPI**: Primary data source
- **Requests**: API communication library
- **uv**: Fast Python package manager and runner
- **Custom in-memory caching system**: Optimized response caching with LRU eviction
- **Smart pagination**: Limits results to 5 items per request, optimizing for AI agent consumption

### Transport Modes

The server supports two transport modes, selected by the `TRANSPORT` environment variable:

1. **Stdio Mode** (`TRANSPORT` unset — the default): MCP communication over standard input/output
   - Used for local MCP clients (Claude Desktop, Claude Code, Cursor, etc.)
   - The API key comes from the `RAPID_API_KEY_IMDB` environment variable

2. **HTTP Mode** (`TRANSPORT=http`): Streamable HTTP transport
   - For self-hosting a shared instance (Docker, or any platform that runs the container)
   - Serves the MCP endpoint at `/mcp`
   - Single-tenant: the API key comes from `RAPID_API_KEY_IMDB` on the server
   - Binds `0.0.0.0:8081` by default (`HOST` / `PORT` environment variables); run it behind a proxy that terminates TLS

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

The cache size and expiration time can be adjusted in `src/imdb_mcp_server/cache.py`:

```python
# Defaults: 600 seconds (10 minutes) and 100 cache keys
# You can customize by modifying the ResponseCache instantiation:
response_cache = ResponseCache(max_size=100, expiry_seconds=600)

# Example with custom values:
# response_cache = ResponseCache(max_size=50, expiry_seconds=120)
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
| API key not recognized | Ensure `RAPID_API_KEY_IMDB` is set — in the `env` block of your MCP client config, your shell, `.env`, or `-e` on the Docker container |
| `ModuleNotFoundError: No module named 'mcp.server.fastmcp'` | You're on an old checkout with `mcp` 2.x installed. Pull the latest (this server targets `mcp` 2.x / `MCPServer`) and run `uv sync` |
| `HTTP 401` / `HTTP 403` from the IMDb API | Your RapidAPI key is invalid or not subscribed to the IMDb API. (Re)subscribe to the [IMDb API](https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236) on RapidAPI and copy the fresh key |
| `HTTP 404` from the IMDb API | The RapidAPI subscription is inactive or the upstream endpoint changed. Check the subscription status on your [RapidAPI dashboard](https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236) |
| The old `npx @smithery/cli install` command fails | Smithery ended free managed hosting (March 2026), so there is no shared remote instance. Install locally instead — see [Installation](#installation) |
| Rate limit exceeded | Check your RapidAPI subscription tier and limits at [RapidAPI Dashboard](https://rapidapi.com/developer/dashboard) |
| Timeout errors | The server has a 30-second timeout; for large requests, try limiting parameters or using pagination |
| Empty results | Try broader search terms or check if the content exists in IMDb's database |
| High memory usage | If running for extended periods with many unique queries, restart the server occasionally to clear the cache |
| Port already in use | Change the port using the `PORT` environment variable (HTTP mode only): `TRANSPORT=http PORT=8082 uv run imdb-server` |
| Import errors | Ensure all dependencies are installed: `uv sync` (or `pip install "mcp[cli]>=2.1,<3" requests`) |
| Connection refused (Docker) | Ensure the container is running: `docker ps` and check the logs: `docker logs imdb_server` |

## License

This MCP server is available under the MIT License.
