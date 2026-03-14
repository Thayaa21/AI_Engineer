# Lesson 4: Descriptors for Data Validation in AI Pipelines

## The Intuition

A descriptor is a **smart form field** 📋

When you fill out a job application, the form itself rejects wrong input:
- Age field? Must be a number
- Experience? Must be between 0 and 50 years

You don't need a human to check — the **form field validates itself**.

That's a descriptor — the attribute validates itself the moment someone tries to set it.

---

## In AI Pipelines

Without descriptors — validation is scattered everywhere, repeated in every `__init__`, easy to miss.

With descriptors — define the rule **once** on the attribute, it enforces itself everywhere.

```python
class ModelConfig:
    learning_rate = ValidatedRange(0.0, 1.0)  # smart field — only accepts 0 to 1
    dropout_rate = ValidatedRange(0.0, 0.5)   # smart field — only accepts 0 to 0.5
```

Someone tries `learning_rate = 5.0` → field rejects instantly. Model never sees bad data.

---

## Three Guards on Every Attribute

| Method | Triggered when |
|--------|---------------|
| `__get__` | Someone **reads** the value |
| `__set__` | Someone **writes** a value — validation happens here |
| `__delete__` | Someone **deletes** the value |

---

## Key Concepts

- `__set_name__` — form field automatically knows its own label (e.g. `"learning_rate"`)
- `instance.__dict__` — where the actual value is stored after validation passes
- Never store value on the descriptor itself (`self.value`) — it gets shared across all instances, causes bugs

---

## Key Takeaways

- Descriptor = smart form field — validates itself on every read/write
- Define validation once, apply to any number of attributes
- In AI: ensures bad hyperparameters, wrong types, out-of-range values never enter your pipeline
- Use for reusable validation — don't overuse for every trivial attribute