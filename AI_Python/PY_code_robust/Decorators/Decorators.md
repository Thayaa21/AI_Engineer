# Advanced Decorators for AI Workflow Management

## The Intuition

Think of a **function as a worker** — a plumber, a mechanic, a specialist. They do one specific job.

A **decorator is a manager** — it wraps around the worker and adds behavior *before or after* the job, without changing the worker itself.

> The plumber still fixes pipes. The manager just makes sure the job is logged, timed, or retried if something goes wrong.

---

## Basic Decorator

```python
import functools

def manager(worker):
    @functools.wraps(worker)      # Preserves the worker's identity
    def wrapper(*args, **kwargs):
        print("Job started")
        result = worker(*args, **kwargs)
        print("Job done")
        return result
    return wrapper

@manager
def plumber():
    print("Fixing pipes")

plumber()
```

**What's happening:**
- `@manager` replaces `plumber` with `wrapper`
- When you call `plumber()`, you're actually calling `wrapper()`, which calls the real plumber inside
- `@functools.wraps(worker)` — tells Python "remember this wrapper is still the original worker" — preserves the function's name and metadata

---

## Advanced Decorator (with arguments)

What if the manager needs **instructions**? Like: *"retry this job 3 times if it fails"*

```python
def manager(retries=3):           # Level 1: manager receives instructions
    def decorator(worker):        # Level 2: decorator receives the worker
        @functools.wraps(worker)
        def wrapper(*args, **kwargs):  # Level 3: wrapper does the actual work
            for attempt in range(retries):
                try:
                    return worker(*args, **kwargs)
                except Exception as e:
                    print(f"Retry {attempt + 1}/{retries} — {e}")
            raise Exception("All retries failed")
        return wrapper
    return decorator

@manager(retries=3)
def run_ai_model():
    print("Running AI model...")
```

**Why 3 levels?**
| Level | Role |
|-------|------|
| `manager(retries)` | Receives the configuration/instructions |
| `decorator(worker)` | Receives the actual function to wrap |
| `wrapper(*args, **kwargs)` | Executes the logic before/after the worker |

---

## Why This Matters for AI

Instead of adding logging, timing, or retry logic to **every single AI function**, one decorator handles all of them:

```python
@log_function_call
def train_model(): ...

@log_function_call
def run_inference(): ...

@log_function_call
def preprocess_data(): ...
```

One manager. Many workers. Clean code.

---

## Real World AI Use Case — Permission Control

Think of it as a **nightclub bouncer** 🎵

- The bouncer (`requires_permission`) stands at the door
- Each room has a **different bouncer** with different rules
- Admin has a **master key** — gets into every room
- The DJ inside (`deploy_model`) doesn't care who's at the door — that's the bouncer's job

```python
import functools

def requires_permission(permission_level: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user_role: str, *args, **kwargs):
            if user_role == permission_level or user_role == "admin":
                print(f"ACCESS GRANTED: '{user_role}' enters '{func.__name__}'")
                return func(user_role, *args, **kwargs)
            else:
                print(f"ACCESS DENIED: '{user_role}' can't enter '{func.__name__}'")
                raise PermissionError(f"Insufficient permissions for '{user_role}'")
        return wrapper
    return decorator

@requires_permission("data_scientist")   # this door = data scientists + admin only
def deploy_model(user_role, model_id, environment):
    print(f"'{user_role}' deploying '{model_id}' to '{environment}'")

@requires_permission("ml_engineer")     # this door = ml engineers + admin only
def update_feature_store(user_role, feature_name, version):
    print(f"'{user_role}' updating '{feature_name}' to '{version}'")
```

**The flow:**
```
requires_permission("data_scientist")  ← sets the door rule
    └── decorator(deploy_model)        ← attaches bouncer to the door
        └── wrapper(user_role, ...)    ← bouncer checks ID every time
```

**Why this matters in AI:**
In production, you don't want a junior analyst accidentally deploying a model.
The decorator **guards** the function — security is the bouncer's job, not the DJ's.

---

## Stacking Decorators

**The Nightclub with a CCTV 🎥🎵**

The worker (DJ) now has TWO managers:
- **Bouncer** (`requires_permission`) — checks ID at the door
- **CCTV** (`logger`) — records everything that happens, including the bouncer's decisions

The CCTV is outside the bouncer — it sees everything first.
So CCTV goes on **top**, bouncer goes **below**.

> Read bottom to top — bottom decorator is closest to the worker, top decorator is the first thing the world hits.

```python
@logger                                  # CCTV — outside, sees everything first
@requires_permission("data_scientist")   # Bouncer — checks ID before worker runs
def deploy_model(user_role, model_id, environment):
    print(f"'{user_role}' deploying '{model_id}' to '{environment}'")
```

Python reads this as:
```
logger( requires_permission( deploy_model ) )
```
Jacket over t-shirt — bottom wraps first, top wraps over that.

```python
@logger                                  # CCTV — outside, sees everything first
@requires_permission("data_scientist")   # Bouncer — checks ID before worker runs
def deploy_model(user_role, model_id, environment):
    ...
```

---

## Class-Based Decorators

**Function decorator = one manager**
**Class decorator = whole management team** — each method has a different role, and the team **remembers everything** using `self`.

A function manager forgets after each job. Class management team keeps records forever.

### The Two Roles

| Method | Role |
|--------|------|
| `__init__` | Front desk — registers the plumber OR receives the rulebook |
| `__call__` | Activates every time plumber gets a job call |

### No Brackets — Plumber registers at `__init__`

```python
@CCTVManager
def deploy_model():
    ...
```
- `__init__` = plumber walks in, management registers him, starts the counter
- `__call__` = every job call, CCTV ticks the counter up

### With Brackets — Rules first, plumber later

```python
@RateLimiter(calls_per_second=0.5)
def query_ai_api():
    ...
```
- `__init__` = management hired with rulebook ("1 job every 2 seconds")
- `__call__` = plumber arrives, gets wrapped with the rules

> **Simple rule — brackets = rules first, plumber later. No brackets = plumber first, job later.**

### Why Class Over Function Decorator?

RateLimiter needs to **remember** the last job time across every call — `self.last_call_time`. A function decorator can't do this, it forgets after each call. Class remembers because of `self`.

---



## Input Validation and Transformation

**The Agency, Bouncer & Makeover Artist 💇🎵**

Instead of putting a big board inside the club (hardcoding rules into the worker), you call the **agency** with the rulebook. Agency briefs the bouncer. Bouncer enforces it. Worker never changes.

- **Validation** = Bouncer checks — wrong type? Too short? Go home!
- **Transformation** = Makeover artist — trim edges, lowercase, remove weird symbols
- Worker only ever sees **clean, valid input**. Never sees the mess.

```python
@club_agency(min_length=20, make_lowercase=True)  # tell agency the rules
def keyword_club(clean_guest):                     # DJ only sees clean guests
    ...
```

**The power — same bouncer agency, different rules per club:**

```python
@club_agency(min_length=20)   # strict club
def keyword_club(): ...

@club_agency(min_length=5)    # chill club
def summary_club(): ...
```

> Tomorrow you want `min_length=50`? Just tell the agency. Worker never changes. Bouncer gets new briefing.

**Why this matters in AI:**
Garbage in, garbage out. Decorator guards and cleans before the model ever sees the input. Worker stays clean, always.

---



**The Receptionist's Notebook 📒**

Building a house — you needed bricks for the ground floor, bought them, used them. Now you need the same bricks for the next floor — why buy new ones? Grab from your own storage!

Same in AI — every model call costs money and time. Cache saves already-done work so the worker never has to redo it.

- `CACHE = {}` = the notebook/storage
- `cache_key` = unique ticket number made from the input
- `CACHE HIT` = answer in notebook, worker sleeps ✅
- `CACHE MISS` = never seen this input, worker studies fresh ❌

```python
if cache_key in CACHE:
    return CACHE[cache_key]         # grab from notebook
else:
    result = func(*args, **kwargs)  # worker studies it
    CACHE[cache_key] = result       # write in notebook for next time
```

> **Careful** — cache is exact match only. Change one word = different ticket number = worker wakes up again.

**Why this matters in AI:**
1000 users ask the same question → run model once → serve 999 from notebook. Saves 💰 money, ⏱️ time, ⚡ compute.

---

## Key Takeaways
- `@functools.wraps` preserves the original function's identity
- Advanced decorators accept arguments → 3 levels of nesting
- In AI: use decorators for logging, timing, retrying, and monitoring model calls