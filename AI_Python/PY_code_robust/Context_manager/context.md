# Lesson 2: Context Managers for Resource-Efficient AI Operations

## The Intuition

A context manager is a **hotel** — guarantees check in AND check out, even if the guest crashes the room (error occurs).

In AI, "resources" = GPU memory, file handles, database connections. Expensive and limited. Forget to release them — blocked forever.

> Context manager guarantees the release, no matter what.

---

## The Hotel Analogy 🏨

- `__enter__` = check in — room prepared, key handed, logged as occupied
- `__exit__` = check out — room cleaned, key taken back, **always happens**
- `yield` = key handed — guest works here (simpler style)
- `finally` = hotel's guarantee — "no matter what, we WILL clean up"

---

## Two Ways to Build a Hotel

### Style 1 — Full Management Firm (Class)

```python
class GPUHotel:
    def __enter__(self):
        # check in — GPU allocated
        return self

    def __exit__(self, error_type, error_value, trace):
        # check out — GPU released, always
        pass
```

### Style 2 — One Manager (`@contextmanager`)

```python
@contextmanager
def gpu_room(room_name):
    print("Check in — GPU allocated 🟢")
    try:
        yield        # 🔑 guest works here
    finally:
        print("Check out — GPU released 🔴")  # always runs
```

Same result — simpler code. `yield` replaces `__enter__`/`__exit__`.

---

## Multiple Rooms — ExitStack 🧹

**Head of housekeeping** — doesn't matter if 1 room or 100, all get cleaned when guests leave.

```python
with ExitStack() as housekeeping:
    files = [housekeeping.enter_context(open(p)) for p in paths]
    # all rooms open, all cleaned automatically
```

Without ExitStack — messy manual nesting. With ExitStack — housekeeping handles all rooms in one go.

---

## Decorator vs Context Manager

| | Decorator | Context Manager |
|---|---|---|
| Job | Wraps worker, adds behavior | Guarantees cleanup |
| Crash? | Doesn't guarantee cleanup | Always cleans up |
| Analogy | Manager around worker | Hotel with guaranteed checkout |

---

## Key Takeaways

- Context manager = hotel — guaranteed checkout no matter what
- `__enter__` = check in, `__exit__` = check out
- `@contextmanager` + `yield` = simpler way to build the hotel
- `ExitStack` = housekeeping for multiple rooms
- In AI: GPU memory, file handles, database connections — always use context managers