import os
import threading
from typing import Optional


class ConfigManager:
    """Manages configuration for both stdio and HTTP modes."""
    
    def __init__(self):
        # Store api key only for stdio mode (backwards compatibility)
        self._api_key: Optional[str] = None
        
        # Thread-local storage for per-request API keys
        self._thread_local = threading.local()
    
    def handle_config(self, config: dict):
        """Handle configuration from Smithery - for backwards compatibility with stdio mode."""
        if api_key := config.get('rapidApiKeyImdb'):
            self._api_key = api_key
        # You can handle other session config fields here
    
    def get_request_config(self) -> dict:
        """Get full config from current request context."""
        try:
            # Access the current request context from FastMCP
            import contextvars
            
            # Try to get from request context if available
            request_context = contextvars.copy_context()
            request = request_context.get('request')
            if hasattr(request, 'scope') and request.scope:
                return request.scope.get('smithery_config', {})
        except Exception as e:
            print(f"Error getting request config: {e}")
            pass
        return {}
    
    def get_config_value(self, key: str, default=None):
        """Get a specific config value from current request."""
        # Try thread-local storage first
        if hasattr(self._thread_local, 'config'):
            return self._thread_local.config.get(key, default)
        
        # Fallback to request context method
        config = self.get_request_config()
        return config.get(key, default)
    
    def set_thread_config(self, config: dict):
        """Set config in thread-local storage."""
        self._thread_local.config = config
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from request context or fallback to global variable."""
        return self.get_config_value('rapidApiKeyImdb') or self._api_key
    
    def initialize_stdio_mode(self):
        """Initialize configuration for stdio mode."""
        api_key = os.getenv("RAPID_API_KEY_IMDB")
        self.handle_config({"rapidApiKeyImdb": api_key})
        return api_key


# Global config manager instance
config_manager = ConfigManager()
