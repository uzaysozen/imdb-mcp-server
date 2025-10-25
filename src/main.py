import os
import sys
import signal
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

# Add the project root to Python path to enable src imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.middleware import SmitheryConfigMiddleware
from src.config import config_manager
from src.tools import register_tools


# Handle SIGINT (Ctrl+C) gracefully
def signal_handler(sig, frame):
    print("Shutting down server gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Initialize FastMCP server
mcp = FastMCP(name="IMDb MCP Server")

# Register all tools
register_tools(mcp)


def main():
    transport_mode = os.getenv("TRANSPORT", "stdio")
    
    if transport_mode == "http":
        # HTTP mode with config extraction from URL parameters
        print("IMDb MCP Server starting in HTTP mode...")
        
        # Setup Starlette app with CORS for cross-origin requests
        app = mcp.streamable_http_app()
        
        # IMPORTANT: add CORS middleware for browser based clients
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["mcp-session-id", "mcp-protocol-version"],
            max_age=86400,
        )

        # Apply custom middleware for config extraction (per-request API key handling)
        app = SmitheryConfigMiddleware(app)

        # Use Smithery-required PORT environment variable
        port = int(os.environ.get("PORT", 8081))
        print(f"Listening on port {port}")

        uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")
    
    else:
        # Optional: add stdio transport for backwards compatibility
        # You can publish this to uv for users to run locally
        print("IMDb MCP Server starting in stdio mode...")
        
        api_key = config_manager.initialize_stdio_mode()
        
        # Run with stdio transport (default)
        print(f"API key: {api_key}")
        mcp.run()


if __name__ == "__main__":
    main()