# doc8-custom-ignores

Configure additional doc8 `D000` ignores in `pyproject.toml`.

## Install

```console
pip install doc8-custom-ignores
```

The plugin is discovered automatically by doc8.

## Configure

Prefer exact messages:

```toml
[tool.doc8]
ignore-messages = [
    """Error in "include" directive:
unknown option: "path-substitutions".""",
]
```

Regular expressions are available when an exact message is not suitable:

```toml
[tool.doc8]
ignore-regex = [
    '''^Error in "include" directive:\nunknown option: "path-substitutions"\.$''',
]
```

Patterns use Python regular-expression syntax. Both settings follow doc8's
default behavior and are disabled by `doc8 --no-sphinx`.

[Source code](https://github.com/adamtheturtle/doc8-custom-ignores)
