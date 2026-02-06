# Design Notes

Behind-the-scenes stories about interesting design challenges encountered while building PyQuantLib.

Binding C++ to Python is often straightforward. But sometimes, a C++ design pattern fundamentally clashes with Python's memory model or object semantics. QuantLib is a sophisticated library with idioms that do not always translate cleanly to Python. These articles capture the non-obvious cases where we had to get creative.

These notes help contributors understand why certain patterns exist in the codebase, give other binding authors lessons from similar challenges, and offer the curious a window into the detective work behind seemingly simple APIs.

```{toctree}
:maxdepth: 1

interpolation
settings-singleton
hidden-handles
bridge-defaults
python-subclassing
```
