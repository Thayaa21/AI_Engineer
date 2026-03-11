import functools

def log_function_call(func):
    """
    A decorator that logs the execution of a function.
    """
    @functools.wraps(func) # Preserves the original function's metadata
    def wrapper(*args, **kwargs):
        print(f"INFO: Calling function '{func.__name__}' with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"INFO: Function '{func.__name__}' finished, returned: {result}")
        return result
    return wrapper

@log_function_call
def train_model(model_name: str, dataset_path: str):
    """
    Simulates a model training process.
    """
    print(f"Training {model_name} on {dataset_path}...")
    # In a real scenario, this would involve complex ML logic
    return f"Model {model_name} trained successfully."

@log_function_call
def preprocess_data(raw_data_path: str, output_path: str, cleaning_level: int = 1):
    """
    Simulates a data preprocessing step.
    """
    print(f"Preprocessing data from {raw_data_path} to {output_path} with cleaning level {cleaning_level}...")
    # In a real scenario, this would involve data cleaning, feature engineering
    return f"Data preprocessed and saved to {output_path}."

# Calling the decorated functions
train_model("ResNet50", "/data/imagenet_mini")
print("-" * 30)
preprocess_data("/raw_data/sensor_logs", "/processed_data/sensor_logs_v1", cleaning_level=2)


import functools

def requires_permission(permission_level: str):
    """
    A decorator factory that creates a decorator to check user permissions.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user_role: str, *args, **kwargs):
            # In a real system, 'current_user_role' would be obtained from session/authentication
            # For this example, we pass it explicitly as the first argument
            if user_role == permission_level or user_role == "admin": # 'admin' always has access
                print(f"PERMISSION: User with role '{user_role}' has access for '{func.__name__}'.")
                return func(user_role, *args, **kwargs) # Pass user_role to the original function if needed
            else:
                print(f"PERMISSION ERROR: User with role '{user_role}' does not have '{permission_level}' permission for '{func.__name__}'.")
                raise PermissionError(f"Insufficient permissions for user role '{user_role}'.")
        return wrapper
    return decorator

@requires_permission("data_scientist")
def deploy_model(user_role: str, model_id: str, environment: str):
    """
    Simulates deploying an AI model to a given environment.
    Only data scientists or admins can perform this.
    """
    print(f"User '{user_role}' deploying model '{model_id}' to '{environment}'.")
    return f"Model {model_id} deployed to {environment}."

@requires_permission("ml_engineer")
def update_feature_store(user_role: str, feature_name: str, new_version: str):
    """
    Simulates updating a feature in the feature store.
    Only ML engineers or admins can perform this.
    """
    print(f"User '{user_role}' updating feature '{feature_name}' to version '{new_version}'.")
    return f"Feature '{feature_name}' updated to version '{new_version}'."

# Test cases
try:
    deploy_model("data_scientist", "fraud_detector_v2", "production")
    deploy_model("admin", "recommendation_engine_v1", "staging")
    update_feature_store("ml_engineer", "user_click_rate", "1.1")
    update_feature_store("admin", "product_embedding_dims", "2.0")
    # This call should fail
    deploy_model("junior_analyst", "sentiment_model_v3", "production")
except PermissionError as e:
    print(e)


import functools

def log_function_call_stack(func):
    """
    A decorator for logging function calls (adapted for stacking).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"LOG (Stack): Calling '{func.__name__}'")
        result = func(*args, **kwargs)
        print(f"LOG (Stack): Finished '{func.__name__}'")
        return result
    return wrapper

def requires_permission_stack(permission_level: str):
    """
    A decorator factory for permission checks (adapted for stacking).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user_role: str, *args, **kwargs):
            if user_role == permission_level or user_role == "admin":
                print(f"PERMISSION (Stack): User '{user_role}' has '{permission_level}' permission for '{func.__name__}'.")
                return func(user_role, *args, **kwargs)
            else:
                print(f"PERMISSION ERROR (Stack): User '{user_role}' lacks '{permission_level}' permission for '{func.__name__}'.")
                raise PermissionError(f"Insufficient permissions for user role '{user_role}'.")
        return wrapper
    return decorator

@log_function_call_stack # Applied second (outermost wrapper)
@requires_permission_stack("ml_engineer") # Applied first (innermost wrapper)
def retrain_model_pipeline(user_role: str, model_id: str, new_dataset_path: str):
    """
    Simulates a full model retraining pipeline.
    Requires ML Engineer permissions and will log its execution.
    """
    print(f"User '{user_role}' initiating retraining for model '{model_id}' with dataset '{new_dataset_path}'.")
    # Complex ML pipeline steps...
    return f"Model '{model_id}' retraining complete."

print("--- Testing stacked decorators (success) ---")
retrain_model_pipeline("ml_engineer", "recommender_v2", "/data/new_interactions")

print("\n--- Testing stacked decorators (permission failure) ---")
try:
    retrain_model_pipeline("data_scientist", "recommender_v2", "/data/new_interactions")
except PermissionError as e:
    print(e)

print("\n--- Order of decorators matters: log then permission ---")
# If @log_function_call_stack was below @requires_permission_stack:
# The log_function_call_stack decorator would receive the result of requires_permission_stack.
# In this current order: log -> permission -> actual_function
# The `log_function_call_stack` decorator wraps the `requires_permission_stack`'s wrapper.
# So, logging happens *before* permission check, then permission check, then actual function.
# If permission fails, the log will show the *attempt* to call, but the actual function won't run.



import functools
import time

class RateLimiter:
    """
    A class-based decorator to limit the rate at which a function can be called.
    Useful for API calls to external AI services.
    """
    def __init__(self, calls_per_second: int):
        self.calls_per_second = calls_per_second
        self.interval = 1.0 / calls_per_second
        self.last_call_time = 0.0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.monotonic()
            elapsed_time = current_time - self.last_call_time

            if elapsed_time < self.interval:
                sleep_time = self.interval - elapsed_time
                print(f"RATE LIMITER: Pausing for {sleep_time:.2f}s before calling '{func.__name__}'...")
                time.sleep(sleep_time)

            self.last_call_time = time.monotonic()
            print(f"RATE LIMITER: Calling '{func.__name__}' at {self.last_call_time:.2f}s.")
            return func(*args, **kwargs)
        return wrapper

@RateLimiter(calls_per_second=0.5) # Allow 0.5 calls per second, i.e., 1 call every 2 seconds
def query_ai_api(query: str):
    """
    Simulates querying an external AI API (e.g., a large language model endpoint).
    """
    print(f"Querying AI API with: '{query}'")
    time.sleep(0.1) # Simulate network latency
    return f"Response for '{query}'"

print("--- Testing RateLimiter decorator ---")
start_time = time.monotonic()
query_ai_api("What is the capital of France?")
query_ai_api("Tell me a joke.")
query_ai_api("Summarize this text.")
end_time = time.monotonic()
print(f"Total execution time: {end_time - start_time:.2f}s")


import functools
import hashlib
import json
import time

# A simple in-memory cache for demonstration.
# In production, this would likely be Redis or a similar key-value store.
CACHE = {}

def cache_predictions(func):
    """
    Decorator to cache the results of a function based on its arguments.
    Useful for expensive AI model inference calls.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique cache key from function name and arguments
        # Simple hashing for demonstration; consider robust serialization for complex objects
        key_parts = [func.__name__] + list(args) + sorted([(k, v) for k, v in kwargs.items()])
        cache_key = hashlib.md5(json.dumps(key_parts, sort_keys=True).encode('utf-8')).hexdigest()

        if cache_key in CACHE:
            print(f"CACHE HIT for '{func.__name__}' with key '{cache_key[:8]}...'")
            return CACHE[cache_key]
        else:
            print(f"CACHE MISS for '{func.__name__}' with key '{cache_key[:8]}...'. Computing...")
            result = func(*args, **kwargs)
            CACHE[cache_key] = result
            return result
    return wrapper

@cache_predictions
def get_sentiment_score(text: str, model_version: str = "v1"):
    """
    Simulates calling a sentiment analysis model. This is an expensive operation.
    """
    print(f"Analyzing sentiment for text: '{text[:20]}...' using model {model_version}")
    time.sleep(1) # Simulate computation time
    # Dummy logic for sentiment score
    if "happy" in text.lower() or "good" in text.lower():
        return {"text": text, "score": 0.9, "model": model_version}
    elif "bad" in text.lower() or "sad" in text.lower():
        return {"text": text, "score": 0.1, "model": model_version}
    else:
        return {"text": text, "score": 0.5, "model": model_version}

print("--- Testing cache_predictions decorator ---")
result1 = get_sentiment_score("This is a really good day!", model_version="v2")
result2 = get_sentiment_score("This is a really good day!", model_version="v2") # Cache hit!
result3 = get_sentiment_score("I am feeling very happy.", model_version="v1")
result4 = get_sentiment_score("I am feeling very happy.", model_version="v1") # Cache hit!
result5 = get_sentiment_score("The movie was bad.", model_version="v2")
print(result1)
print(result2)
print(result3)
print(result4)
print(result5)