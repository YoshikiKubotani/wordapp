## Python version constraints

When implementing Python code, use the notation of version 3.10.

e.g.

- Bad:

  ```python
  from typing import List

  var: List[str] = ["hoge", "fuga"]
  ```

- Good:

  ```python
  var: list[str] = ["hoge", "fuga"]
  ```

## Types and Docstrings

Make sure to add type annotations for every variable, and to add complete docstrings to all classes/methods in a Google style (DO NOT omit some parts).

## Path representation

Use pathlib library instead of os library.

## Data class representation

Use pydantic model for any data class representation.
