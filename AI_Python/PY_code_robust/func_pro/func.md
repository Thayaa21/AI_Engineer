# Lesson 5: Functional Programming Patterns for AI Data Transformations

## The Intuition

Functional programming = **let the function signature handle everything, not the developer**

No hidden state, no surprises, no bugs from things changing outside your function.

---

## Pure Functions — The Vending Machine 🎰

Press B3 → always get chips. Every time. No surprises.

A pure function = same input, always same output. Doesn't touch anything outside itself.

```python
# Impure — depends on outside world, unpredictable waiter
GLOBAL_MEAN = 0.5
def impure_scale(x):
    return x - GLOBAL_MEAN  # what if GLOBAL_MEAN changes? bug!

# Pure — vending machine, never lies
def pure_scale(x, mean):
    return x - mean  # same x + mean = always same result
```

> Pure functions + caching = free speed boost. Same input? Grab from notebook, never recompute.

---

## Map, Filter, Reduce — The Food Factory 🏭

Conveyor belt: raw vegetables come in, clean data comes out.

- **Map** = transformer — touches every item, changes it. Nothing removed.
- **Filter** = quality checker — removes bad items, only good ones pass.
- **Reduce** = blender — takes everything left, combines into ONE result.

```python
raw = [1.2, 0.8, 2.5, -1.0, 3.1]

normalized = list(map(lambda x: x / 10.0, raw))     # transform all
valid      = list(filter(lambda x: x > 0, normalized))  # remove bad
total      = reduce(lambda acc, x: acc + x, valid, 0.0) # combine into one
```

> List comprehensions work for map and filter. `reduce` has no equivalent — always use it for combining into one value.

---

## Function Composition — The Assembly Line 🔧

Chain small single-purpose workers into one big pipeline. Swap, reorder, or test any worker independently.

```python
add_bias = lambda x: x + 1.0
scale    = lambda x: x * 0.5
clip     = lambda x: max(0, min(1, x))

# Assembly line — workers run right to left (add_bias first, clip last)
process_feature = compose(clip, scale, add_bias)
```

> Like putting on clothes — bottom to top. Same stacking rule as decorators.

---

## Generators — The Conveyor Belt That Never Ends 🏗️

Loading 10 million rows into memory = 💥 OOM crash.

Generator = conveyor belt that produces **one item at a time**. Never loads everything. Constant memory.

```python
def stream_features(data):
    for item in data:
        yield item * 0.5  # produce one, pause, wait for next request
```

- `yield` = "here's one item, I'll wait for you to ask for the next"
- Generator never loads the full dataset — just knows how to produce items

> In AI: process item by item, model never waits for full dataset to load.

---

## Key Takeaways

- Pure function = vending machine — same input, same output, no side effects
- Map = transform all, Filter = remove bad, Reduce = combine into one
- Function composition = assembly line of small workers chained together
- Generators = conveyor belt — one item at a time, never the whole factory
- In AI: functional patterns = less bugs, easier to test, safe for parallel execution