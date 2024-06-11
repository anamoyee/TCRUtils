import pathlib as p

from .discord.tcrd_string import get_token

# Get the test.py file contents if any and execute them.
TESTFILE = get_token(filename='test.py', depth=0, dont_strip=True)
exec(TESTFILE)
