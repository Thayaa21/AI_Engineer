# Lesson 6: Pythonic Packaging and Distribution for AI Libraries

## The Intuition

You've built an amazing AI tool. **Packaging = putting it in a proper box** so others can `pip install` it and use it instantly.

> Without packaging — your code lives only on your machine. With packaging — anyone in the world can install and use it in one command.

---

## The Box Label — `pyproject.toml`

`pyproject.toml` = the label on the box — tells pip what's inside, what it needs, how to install it.

```toml
[project]
name = "my-ai-model"
version = "0.1.0"
dependencies = [
    "numpy>=1.24.0",
    "torch>=2.0.0",
]
```

Replaces the old `setup.py` — cleaner, safer, no arbitrary code execution.

---

## The Folder Structure

```
my_ai_model/
├── pyproject.toml       # box label
├── src/                 
│   └── my_ai_model/     # actual code lives here
│       ├── __init__.py
│       └── core.py
├── tests/               # test suite
└── README.md
```

`src/` layout = best practice — forces you to properly install before testing. Prevents sneaky bugs where tests run against wrong code.

---

## Optional Dependencies — Choose Your Box Size

Not everyone needs GPU support. Let users install only what they need:

```toml
[project.optional-dependencies]
dev = ["pytest", "black"]      # for developers
gpu = ["torch-cuda"]           # for GPU users
```

```bash
pip install my-ai-model          # lightweight, CPU only
pip install my-ai-model[gpu]     # full GPU support
```

---

## Namespace Packages — Company Umbrella ☂️

Multiple AI libraries, one company name:

```python
import company.nlp      # from company-nlp package
import company.vision   # from company-vision package
```

Different repos, same namespace. Just omit `__init__.py` in the top-level folder — Python merges them automatically.

---

## Key Takeaways

- `pyproject.toml` = modern box label for your package
- `src/` layout = best practice folder structure
- Optional dependencies = users install only what they need
- Namespace packages = multiple libraries under one company umbrella
- You'll need this when you're ready to ship an AI library to others