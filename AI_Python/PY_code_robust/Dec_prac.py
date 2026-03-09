import functools

### A simple decorator to manage workers ###

# def manager(worker):
#     @functools.wraps(worker)      # Preserves the worker's identity
#     def wrapper(*args, **kwargs):
#         print("Job started",args, kwargs)
#         result = worker(*args, **kwargs)
#         print("Job done")
#         return result
#     return wrapper

# @manager
# def plumber(price, time):
#     print("Fixing pipes", "amount:", price*time)

# @manager
# def electrician():
#     print("Fixing wires")

# plumber(20,3)
# print(plumber.__name__)
# electrician()
# print(electrician.__name__)

### A decorator to check for permissions ###


def requires_permission(permission_level: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user_role: str, *args, **kwargs):
            if user_role == permission_level or user_role == "admin":
                print(f"ACCESS GRANTED: '{user_role}' enters '{func.__name__}'")
                return func(user_role, *args, **kwargs)
            else:
                print(f"ACCESS DENIED: '{user_role}' can't enter '{func.__name__}'")
                # raise PermissionError(f"Insufficient permissions for '{user_role}'")
        return wrapper
    return decorator

@requires_permission("data_scientist")
def deploy_model(user_role, model_id, environment):
    print(f"'{user_role}' deploying '{model_id}' to '{environment}'")

# Test it
deploy_model("data_scientist", "fraud_v2", "production")  # ✅
deploy_model("admin", "rec_engine", "staging")            # ✅ master key
# try:
deploy_model("junior_analyst", "model_x", "production")
# except PermissionError as e:
#     print(f"Caught: {e}")