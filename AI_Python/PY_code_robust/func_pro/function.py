from functools import reduce, lru_cache
from typing import Callable, Any

# ═══════════════════════════════════════
# PURE FUNCTIONS — Vending Machine 🎰
# Same input, always same output. No surprises.
# ═══════════════════════════════════════

# Impure — depends on outside world, unpredictable waiter
GLOBAL_MEAN = 0.5
def impure_scale(x):
    return x - GLOBAL_MEAN  # what if GLOBAL_MEAN changes? bug!

# Pure — everything passed in, vending machine never lies
def pure_scale(x, mean):
    return x - mean  # same x + mean = always same result

print("--- Pure vs Impure ---")
print(pure_scale(1.0, 0.5))   # always 0.5, no surprises
print(impure_scale(1.0))       # depends on GLOBAL_MEAN — dangerous!

# Pure functions + caching = free speed boost
# Same input? Don't recompute, grab from notebook
@lru_cache(maxsize=128)
def expensive_transform(x, mean, std):
    # Simulates expensive AI feature transformation
    return (x - mean) / std

print("\n--- Caching pure functions ---")
print(expensive_transform(1.0, 0.5, 0.1))  # computed
print(expensive_transform(1.0, 0.5, 0.1))  # from cache — free!


# ═══════════════════════════════════════
# MAP, FILTER, REDUCE — The Food Factory 🏭
# Conveyor belt: transform → filter → combine
# ═══════════════════════════════════════

raw_features = [1.2, 0.8, 2.5, -1.0, 3.1]

# Map — transformer, every item gets changed, nothing removed
normalized = list(map(lambda x: x / 10.0, raw_features))
# same as: [x / 10.0 for x in raw_features]

# Filter — quality checker, bad items thrown out
valid = list(filter(lambda x: x > 0, normalized))
# same as: [x for x in normalized if x > 0]

# Reduce — blender, everything combined into ONE result
total = reduce(lambda acc, x: acc + x, valid, 0.0)
# acc = running total, x = next item on belt

print("\n--- Food Factory Pipeline ---")
print(f"Raw:        {raw_features}")
print(f"Normalized: {normalized}")
print(f"Valid only: {valid}")
print(f"Total sum:  {total}")


# ═══════════════════════════════════════
# FUNCTION COMPOSITION — The Assembly Line 🔧
# Chain small workers into one big pipeline
# ═══════════════════════════════════════

# The assembly line manager — chains workers right to left
def compose(*workers: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def pipeline(raw_input):
        for worker in reversed(workers):  # right to left, like putting on clothes
            raw_input = worker(raw_input)
        return raw_input
    return pipeline

# Small single-purpose workers
add_bias = lambda x: x + 1.0    # worker 1 — adds bias
scale    = lambda x: x * 0.5    # worker 2 — scales down
clip     = lambda x: max(0, min(1, x))  # worker 3 — clips to valid range

# Assemble the pipeline — right to left: add_bias first, clip last
process_feature = compose(clip, scale, add_bias)

dataset = [0.1, 0.5, 2.0]
clean_data = [process_feature(x) for x in dataset]

print("\n--- Assembly Line ---")
print(f"Raw dataset:   {dataset}")
print(f"Clean dataset: {clean_data}")


# ═══════════════════════════════════════
# GENERATORS — The Conveyor Belt That Never Ends 🏗️
# Don't load everything into memory — produce one item at a time
# ═══════════════════════════════════════

# Normal list — loads EVERYTHING into memory at once
# big_list = [process(x) for x in massive_dataset]  # 💥 OOM error!

# Generator — produces one item at a time, constant memory
def stream_features(data):
    # Conveyor belt — one item at a time, never the whole factory
    for item in data:
        yield item * 0.5  # produce one, pause, wait for next request

# Simulating a massive dataset
massive_data = range(1, 1000000)  # 1 million items

# Generator doesn't load 1 million items — just knows how to produce them
feature_stream = stream_features(massive_data)

print("\n--- Generator Stream ---")
print(f"First item:  {next(feature_stream)}")  # produce item 1
print(f"Second item: {next(feature_stream)}")  # produce item 2
print(f"Third item:  {next(feature_stream)}")  # produce item 3
# 999,997 items still waiting — none loaded into memory!

# In real AI — process item by item, model never waits for full dataset
print("\nProcessing first 5 features from stream:")
for i, feature in enumerate(stream_features([1.0, 2.0, 3.0, 4.0, 5.0])):
    print(f"  Model received: {feature}")