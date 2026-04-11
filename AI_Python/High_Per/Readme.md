# Module 2: High-Performance Python for AI

## The Core Problem
Python is an interpreter language — line by line, dynamic typing, heap-allocated objects. C speaks directly to machine. Python goes through layers. This module is about closing that gap.

---

## Lesson 1: The GIL

**What it solves:** Python's memory system isn't safe for multiple workers touching the same object simultaneously.

Every Python object has a reference counter. Two threads decrementing it simultaneously = corruption = segfault. GIL says one thread touches Python objects at a time. Brutal but safe.

**The hotel key analogy:** 8 rooms (cores), one key (GIL). Even if all rooms are empty, next guest waits for the key. 8 cores, 1 doing actual work.

**Two types of tasks:**
| | CPU-bound | I/O-bound |
|---|---|---|
| Example | Training, matrix math | API calls, file reads |
| GIL impact | 🔴 Cores wasted | 🟢 GIL releases while waiting |
| Solution | Multiprocessing | Threading / Asyncio |

**Crucial insight:** NumPy/PyTorch release the GIL during C++ computation — already parallel. GIL only hurts pure Python loops. If your code is moving tensors, GIL is irrelevant.

**Detect GIL contention:** 16 cores, only 1 at 100% = GIL is the problem.

---

## Lesson 2: Multithreading vs Multiprocessing

**Thread** = one instruction stream flowing through a core. Same process, same memory, own PC + stack.

**Multithreading** = multiple instruction streams, shared memory. Fast context switch, but GIL serializes CPU work. Good for I/O only.

**Multiprocessing** = multiple processes, separate memory spaces. Each process has own GIL — true parallelism for CPU work. Higher memory cost.

```
I/O bottleneck → threading
CPU bottleneck, pure Python → multiprocessing
Already using PyTorch/NumPy → neither, already parallel
```

---

## Lesson 3: Asyncio

**What it solves:** Don't sit idle waiting for API responses — go do something else.

**Analogy:** Chef calls warehouse (API). Sync chef stands by phone, kitchen stops. Async chef puts phone on hold, keeps chopping, checks back when warehouse calls. Same chef, smarter waiting.

- `async def` = pauseable function
- `await` = "I'm blocked, event loop take over"
- `gather` = start all tasks simultaneously, total time = slowest task not sum
- `run_in_executor` = escape hatch for blocking libraries — offload to thread pool

**The one rule:** Async = I/O only. CPU task inside async = entire event loop freezes.

**Call stack must be fully async** — one `requests.get()` anywhere = entire loop blocked.

```
API/DB/network wait → asyncio
Multiple threads, shared memory → threading
CPU heavy, pure Python → multiprocessing
```

---

## Lesson 4: Cython

**What it solves:** Pure Python hot loops are slow because every operation goes through the Python object system — type checking, reference counting, heap allocation.

**Analogy:** Python chef translates recipe line by line at runtime. Cython chef has recipe pre-printed in machine instructions — no translation needed.

**Pipeline:** `.pyx` file → Cython compiler → C code → C compiler → `.so` binary → Python imports it.

- `cdef int i` = stack-allocated C integer, no Python object overhead
- `double[:]` memoryview = direct pointer into NumPy buffer, no copying
- `with nogil:` = release GIL inside Cython, true parallelism

**When to use:**
- Pure Python hot loop that NumPy can't vectorize ✅
- Already using NumPy/PyTorch ❌
- Calling frequently with tiny inputs ❌ — boundary conversion kills the gain

---

## Lesson 5: Numba

**What it solves:** Same as Cython but without the build setup — JIT compiles at runtime automatically.

**Analogy:** Cython = pre-printed recipe. Numba = chef reads recipe once, memorizes perfectly, executes from memory every time after. First time slow, every time after instant.

- `@jit(nopython=True)` = strict mode, full machine code, no interpreter fallback
- `@njit(parallel=True)` + `prange` = spread loop across all cores, bypasses GIL
- First call = compilation overhead — always warm up with a dummy call in production

**Cython vs Numba:**
| | Cython | Numba |
|---|---|---|
| Setup | Separate build step | Just a decorator |
| Control | Fine-grained | Automatic |
| Best for | Production libraries | Research, notebooks |

**Strict diet:** Only eats NumPy arrays and arithmetic. Dicts, class instances, lists-of-lists = falls back to slow mode.

---

## Lesson 6: Performance Profiling

**What it solves:** Never optimize blind — measure first, fix the actual bottleneck.

**Analogy:** Restaurant is slow. Don't renovate the whole kitchen — check CCTV first. Find the actual jam. Fix only that.

**Tools:**
- **cProfile** = CCTV timestamping every function call. `cumtime` = total including sub-calls. `tottime` = function alone. High `cumtime`, low `tottime` = bottleneck is inside its sub-calls.
- **memory_profiler** = water meter per line. `Increment` column = memory added by that one line.
- **Flame graph** = bird's eye view. Wider bar = more time spent there.

**Fix order — always in this sequence:**
```
1. Vectorize — replace loops with NumPy/PyTorch
2. Fix algorithm — O(N²) → O(NlogN) beats any micro-optimization
3. Generators — stop loading everything into memory
4. Cython/Numba — last resort, verified hot loops only
```

**The rule:** 20% of code = 80% of execution time. Optimize only what the profiler confirms is slow.

---

## Module 2 Decision Tree

```
Bottleneck is I/O wait? → asyncio
Bottleneck is CPU, pure Python loops? → multiprocessing + Cython/Numba
Already using PyTorch/NumPy? → already parallel, GIL irrelevant
Multiple tasks, shared memory, I/O? → threading
Don't know where bottleneck is? → cProfile first, always
```