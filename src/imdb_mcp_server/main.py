import os
import signal
import sys
from importlib.metadata import PackageNotFoundError, version

from mcp.server.mcpserver import MCPServer

from .tools import register_tools

try:
    __version__ = version("imdb-mcp-server")
except PackageNotFoundError:  # running from a source tree that isn't installed
    __version__ = "0.0.0"


def create_server() -> MCPServer:
    """Create and configure the IMDb MCP server."""
    server = MCPServer("IMDb MCP Server", version=__version__)
    register_tools(server)
    return server


def _handle_sigint(sig, frame):
    # Diagnostics go to stderr so they never corrupt the stdio JSON-RPC stream.
    print("Shutting down server gracefully...", file=sys.stderr)
    sys.exit(0)


def main() -> None:
    signal.signal(signal.SIGINT, _handle_sigint)

    server = create_server()

    if not os.getenv("RAPID_API_KEY_IMDB"):
        print(
            "Warning: RAPID_API_KEY_IMDB is not set. Tool calls will fail until it is configured.",
            file=sys.stderr,
        )

    if os.getenv("TRANSPORT", "stdio") == "http":
        # Self-hosted HTTP mode. Auth is the RAPID_API_KEY_IMDB env var on the
        # server; put the process behind a proxy that terminates TLS.
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8081"))
        print(
            f"IMDb MCP Server starting in HTTP mode on {host}:{port} (MCP endpoint: /mcp)",
            file=sys.stderr,
        )
        server.run(transport="streamable-http", host=host, port=port)
    else:
        print("IMDb MCP Server starting in stdio mode...", file=sys.stderr)
        server.run()


if __name__ == "__main__":
    main()
