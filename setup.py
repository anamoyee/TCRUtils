import os
import pathlib as p

import setuptools

SOURCE_URL = 'https://github.com/TheCreatorrr333/TCRUtils'  # Placeholder

DEPENDENCIES = [
  'colored',
  'hikari',
  'hikari-toolbox',
]

version = p.Path(
  rf'C:\Users\{os.getlogin()}\Desktop\Programming Projects\python\PACKAGES\TCRUtils\VERSION.txt'
).read_text()

setuptools.setup(
  name='tcrutils',
  version=version,
  description='Useful stuff for TCR projects!',
  long_description=p.Path('README.md').read_text(),
  long_description_content_type='text/markdown',
  url=SOURCE_URL,
  author='TheCreatorrrr',
  license='GPL-3.0 license',
  project_urls={
    'Source': SOURCE_URL,
  },
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Utilities',
  ],
  python_requires='>=3.11,<3.12',
  install_requires=DEPENDENCIES,
  packages=setuptools.find_packages(),
  include_package_data=True,
)
