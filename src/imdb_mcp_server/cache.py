from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any
import threading
import time


class ResponseCache:
    """In-memory cache with LRU eviction and automatic expiration."""
    
    def __init__(self, max_size=100, expiry_seconds=600):
        self.cache = OrderedDict[Any, Any]()
        self.max_size = max_size
        self.expiry_seconds = expiry_seconds
    
    def get(self, key):
        """Get cached data if not expired."""
        if key in self.cache:
            _, data = self.cache[key]
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return data
        return None
    
    def set(self, key, data):
        """Set cached data with timestamp."""
        # Check if we need to remove oldest items
        if len(self.cache) >= self.max_size:
            # Remove oldest item (first in OrderedDict)
            self.cache.popitem(last=False)
        
        self.cache[key] = (datetime.now(), data)
        # Move to end (most recently used)
        self.cache.move_to_end(key)
    
    def clear_expired(self):
        """Clear expired cache entries."""
        now = datetime.now()
        expired_keys = [
            key for key, (timestamp, _) in self.cache.items()
            if now - timestamp >= timedelta(seconds=self.expiry_seconds)
        ]
        for key in expired_keys:
            del self.cache[key]


class CacheManager:
    """Manages cache instance and cleanup."""
    
    def __init__(self, max_size=100, expiry_seconds=600, cleanup_interval_minutes=5):
        self.cache = ResponseCache(max_size, expiry_seconds)
        self.last_cache_cleanup = datetime.now()
        self.cleanup_interval = timedelta(minutes=cleanup_interval_minutes)
        self._start_cleanup_thread()
    
    def _start_cleanup_thread(self):
        """Start background thread for periodic cache cleanup."""
        def clear_cache_periodically():
            while True:
                time.sleep(self.cleanup_interval.seconds)
                self.cache.clear_expired()
                print(f"Cache cleaned at {datetime.now().strftime('%H:%M:%S')}")
        
        cache_cleaner = threading.Thread(target=clear_cache_periodically, daemon=True)
        cache_cleaner.start()
    
    def cleanup_if_needed(self):
        """Check if cleanup is needed and perform it."""
        if datetime.now() - self.last_cache_cleanup > self.cleanup_interval:
            self.cache.clear_expired()
            self.last_cache_cleanup = datetime.now()
            print(f"Cache cleaned at {datetime.now().strftime('%H:%M:%S')}")


# Global cache manager instance
cache_manager = CacheManager()
