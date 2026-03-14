# Lesson 3: Metaclasses for Customizing AI Model Behavior

## The Intuition

You already know:
- **Function** = worker (plumber)
- **Class** = factory that builds workers (plumbing firm)
- **Metaclass** = the construction company that builds the firm itself

> Before the firm can hire anyone, someone built the office and set the rules of how every firm must be structured. That's the metaclass.

---

## Side by Side

| | Function | Class | Metaclass |
|---|---|---|---|
| **What it is** | The plumber | The plumbing firm | Construction company that builds firms |
| **What it creates** | Does a job | Creates workers | Creates classes/factories |
| **Runs when?** | When called | When instantiated | Before class even exists |

---

## The Key Idea

Python secretly uses a metaclass called `type` every time you create a class. You've been using it without knowing.

```python
class Firm:
    pass

print(type(Firm))  # <class 'type'> — type built this firm silently
```

A custom metaclass lets you **enforce rules on every class before it opens** — like a building inspector checking the office before the firm can operate.

---

## In AI

Libraries like PyTorch and TensorFlow use metaclasses under the hood to enforce that every model has the right structure. You'll encounter them, rarely write them.

---

## Key Takeaways

- Metaclass = factory that builds factories
- `type` is Python's default metaclass — always running silently
- Used to enforce rules on classes before they even open
- In AI: PyTorch, TensorFlow use them under the hood — you'll see them, rarely write them