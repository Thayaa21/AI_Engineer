import time
import functools
import random

# Your retry decorator here
def retry(max_retries, delay_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt failed: {e}")
                    time.sleep(delay_seconds)
            raise Exception("All retry attempts failed.")
        return wrapper
    return decorator

@retry(max_retries=5, delay_seconds=0.5)
def fetch_remote_resource(url: str):
    """
    Simulates fetching a resource that might fail temporarily.
    Fails randomly 70% of the time.
    """
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to fetch {url}. Connection unstable.")
    print(f"Successfully fetched resource from {url}.")
    return {"status": "success", "url": url}


try:
    fetch_remote_resource("http://api.ai-service.com/data")
except ConnectionError as e:
    print(f"Final failure after retries: {e}")