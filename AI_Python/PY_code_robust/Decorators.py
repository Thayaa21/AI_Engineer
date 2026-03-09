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