"""### This code was not written by me, however it's licensed with the MIT License which allows for free copy and sublicensing of the licensed material.

This code was written by [James Murphy](https://github.com/jamesmurphy-mc) from [MCoding](https://github.com/mCodingLLC/) ([YouTube](https://www.youtube.com/@mCoding))

[Original Source Code](https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/133_cloud_imports/cloud_imports.py)

Copy of the original license (applies only to this file):

```txt
MIT License

Copyright (c) 2022 MCODING, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Small modifications were made to this code
"""
import ast
import importlib.abc
import importlib.machinery
import sys
import types

from ..src.tcr_console import console as c


def is_valid_python_source(code: str) -> bool:
  try:
    ast.parse(code)
  except SyntaxError:
    return False
  else:
    return True


class CloudFinder(importlib.abc.MetaPathFinder):
  def __init__(self, base_url):
    self.base_url = base_url

  def find_spec(self, fullname, path, target=None):
    spec = self._find_py_file_spec(fullname)
    if spec is not None:
      return spec

    spec = self._find_package_init_spec(fullname)
    if spec is not None:
      return spec

    return None

  def _find_py_file_spec(self, fullname):
    url = f"{self.base_url}/{fullname.replace('.', '/')}.py"
    source = self._get_remote_python_source(url)
    if source is None:
      return None
    loader = CloudLoader(fullname, source, url)
    return importlib.machinery.ModuleSpec(fullname, loader, origin=url)

  def _find_package_init_spec(self, fullname):
    url = f"{self.base_url}/{fullname.replace('.', '/')}/__init__.py"
    source = self._get_remote_python_source(url)
    if source is None:
      return None
    loader = CloudLoader(fullname, source, url)
    return importlib.machinery.ModuleSpec(
      fullname,
      loader,
      origin=url,
      is_package=True,
    )

  def _get_remote_python_source(self, url):
    try:
      import requests
    except ImportError:
      c.error('You need to install requests to use tcr.cloud_imports: pip install requests')
      c.error('I am not adding this as dependency because this is a joke module...')
      raise
    try:
      response = requests.get(url)
      response.raise_for_status()
    except requests.HTTPError:
      return None

    source = response.text

    if not is_valid_python_source(source):
      return None
    return source


class CloudLoader(importlib.abc.Loader):
  def __init__(self, fullname, source_code, url):
    self.fullname = fullname
    self.source_code = source_code
    self.url = url

  def create_module(self, spec):
    module = sys.modules.get(spec.name)
    if module is None:
      module = types.ModuleType(spec.name)
      sys.modules[spec.name] = module
    return module

  def exec_module(self, module):
    module.__file__ = self.url
    exec(self.source_code, module.__dict__)
    return module

  def get_source(self, name):
    return self.source_code


def add_repo(url: str):
  sys.meta_path.append(CloudFinder(url))


def add_gh_repo(username: str, repo: str, ref: str):
  add_repo(f'https://raw.githubusercontent.com/{username}/{repo}/{ref}')
