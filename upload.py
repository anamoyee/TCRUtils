import os
import pathlib as p
import shutil
import sys

# repository = [*sys.argv, None][1] or 'pypi'
# repository = repository.rstrip('/\\')

# for x in [' ', '"', "'"]: assert x not in repository

version = [*sys.argv, None][1] or None

if version is not None:
  with open('VERSION.txt', 'w') as f:  # noqa: PTH123
    f.write(version)
else:
  with open('VERSION.txt') as f:  # noqa: PTH123
    a = f.read()
  with open('VERSION.txt', 'w') as f:  # noqa: PTH123
    a = a.split('.')
    a[2] = str(int(a[2]) + 1)
    f.write('.'.join(a))
    print(f'Updated version to {".".join(a)!r}')

try:
  shutil.rmtree('dist')
  os.mkdir('dist')  # noqa: PTH102
  os.system('py -m build')
  os.system('py -m twine upload --repository pypi dist/*')
except KeyboardInterrupt:
  sys.exit()
