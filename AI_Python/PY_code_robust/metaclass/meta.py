class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        # Enforce structural requirements
        if 'forward' not in dct:
            raise TypeError(f"Model {name} must implement 'forward' method")
        if 'input_shape' not in dct:
            raise TypeError(f"Model {name} must define 'input_shape'")
        
        # Modify the class attributes (e.g., auto-registering)
        dct['_registry_id'] = f"model_{name.lower()}"
        return super().__new__(cls, name, bases, dct)

class BaseAIModel(metaclass=ModelMeta):
    pass

# This raises TypeError immediately upon definition
class InvalidModel(BaseAIModel):
    pass 