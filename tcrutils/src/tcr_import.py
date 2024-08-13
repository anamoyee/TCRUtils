import importlib.util
import pathlib as p
from types import ModuleType


def load_package_dynamically(path: p.Path | str) -> ModuleType:
  """Load a python package dynamically from disk. Warning: This executes the file contents as python code.

  It must be either a file with python code (not necessarily `.py` but if you exec user's input it's your fault) or a directory with an __init__.py file.

  Return the imported module.
  """
  pymodule_name = path.stem
  spec = importlib.util.spec_from_file_location(pymodule_name, str(path if path.is_file() else (path / '__init__.py')))
  pymodule = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(pymodule)

  return pymodule
