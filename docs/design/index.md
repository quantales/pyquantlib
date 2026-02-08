# Design Notes

Behind-the-scenes stories about design challenges encountered while building PyQuantLib.

Each note covers a specific problem: the symptoms, the investigation, the failed attempts, and the solution. They document why certain patterns exist in the codebase and offer other binding authors lessons from similar challenges.

For a high-level overview of the tensions that shaped PyQuantLib's architecture, see {doc}`/architecture`.

```{toctree}
:maxdepth: 1

api-design
interpolation
settings-singleton
hidden-handles
bridge-defaults
python-subclassing
protected-members
enum-singletons
cross-tu-holders
diamond-inheritance
builder-pattern
```
