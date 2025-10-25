import os
import sys
import signal
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery
from .tools import register_tools


# Configuration schema for session
class ConfigSchema(BaseModel):
    rapidApiKeyImdb: str = Field(..., description="RapidAPI API key for accessing the IMDb API")


@smithery.server(config_schema=ConfigSchema)
def create_server():
    """Create and configure the MCP server."""
    
    # Create your FastMCP server as usual
    server = FastMCP("IMDb MCP Server")
    
    # Register all tools with the server
    register_tools(server)
    
    return server


# Handle SIGINT (Ctrl+C) gracefully
def signal_handler(sig, frame):
    print("Shutting down server gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def main():
    transport_mode = os.getenv("TRANSPORT", "stdio")
    
    if transport_mode == "http":
        # HTTP mode - Smithery handles the server creation and configuration
        print("IMDb MCP Server starting in HTTP mode...")
        
        # Get the server from Smithery decorator
        server = create_server()

        # Use Smithery-required PORT environment variable
        port = int(os.environ.get("PORT", 8081))
        print(f"Listening on port {port}")

        # Smithery handles the HTTP app setup and CORS automatically
        import uvicorn
        app = server.streamable_http_app()
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    
    else:
        # Stdio mode for backwards compatibility
        print("IMDb MCP Server starting in stdio mode...")
        
        # Create server without Smithery decorator for stdio mode
        server = FastMCP("IMDb MCP Server")
        register_tools(server)
        
        # Run with stdio transport (default)
        api_key = os.getenv("RAPID_API_KEY_IMDB")
        print(f"API key: {api_key}")
        server.run()


if __name__ == "__main__":
    main()