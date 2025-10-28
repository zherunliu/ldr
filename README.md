use of uv package manager

```bash
uv init project_name
uv add dependency_name
uv run main.py
uv sync

uv tool install dependency_name # install to global
uv tool uninstall dependency_name

uvx dependency_name # temporary use

uv init --script main.py # create temporary env with main script
```

[uv, ruff](https://docs.astral.sh/)
