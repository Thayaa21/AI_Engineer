import functools
import time

# The Management Team — remembers everything about the plumber
class CCTVManager:
    def __init__(self, func):
        # Plumber registers at the front desk — management takes note
        self.func = func
        self.call_count = 0        # front desk counter — total jobs taken

    def __call__(self, *args, **kwargs):
        # Every time plumber gets a job call — management activates
        self.call_count += 1
        print(f"CCTV: '{self.func.__name__}' on job #{self.call_count}")
        return self.func(*args, **kwargs)

# HR Policy — plumber can only take 1 job every 2 seconds
class RateLimiter:
    def __init__(self, calls_per_second):
        # Management hired with rulebook — no plumber yet
        self.interval = 1.0 / calls_per_second
        self.last_call_time = 0.0   # remembers last job time

    def __call__(self, func):
        # Now plumber is assigned to this management team
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.monotonic() - self.last_call_time
            if elapsed < self.interval:
                wait = self.interval - elapsed
                print(f"HR: Too soon! Plumber must wait {wait:.2f}s")
                time.sleep(wait)
            self.last_call_time = time.monotonic()
            print(f"HR: Plumber approved for job!")
            return func(*args, **kwargs)
        return wrapper

# No brackets — plumber registers at init
@CCTVManager
def deploy_model():
    print("Deploying model...")

# With brackets — rules first, plumber later
@RateLimiter(calls_per_second=0.5)
def query_ai_api(query):
    print(f"Querying AI: '{query}'")

# Test CCTV
deploy_model()
deploy_model()
deploy_model()

print("---")

# Test RateLimiter — watch the waiting!
query_ai_api("What is AI?")
query_ai_api("Tell me a joke.")