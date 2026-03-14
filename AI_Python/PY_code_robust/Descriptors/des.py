# The smart form field — validates before accepting anything
class ValidatedRange:
    def __set_name__(self, owner, name):
        self.name = name          # form field knows its own label
        self.min_val = 0.0
        self.max_val = 1.0

    def __set__(self, instance, value):
        # Guard — reject bad values before storing
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        instance.__dict__[self.name] = value  # store only if valid

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)  # return stored value

# The AI model config form — each field guards itself
class ModelConfig:
    learning_rate = ValidatedRange()  # smart form field
    dropout_rate = ValidatedRange()   # smart form field

    def __init__(self, lr, dropout):
        self.learning_rate = lr    # __set__ triggers here
        self.dropout_rate = dropout

# Valid
config = ModelConfig(0.01, 0.3)
print(config.learning_rate)  # __get__ triggers here

# Invalid — form rejects it
try:
    config.learning_rate = 5.0
except ValueError as e:
    print(f"FORM REJECTED: {e}")