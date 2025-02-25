import pathlib as p

import pytest
from tcrutils.console import c


def test_pyrootfile():
	from tcrutils.path import pyrootfile

	assert pyrootfile() == p.Path("<frozen runpy>")


def test_pyrootdir():
	from tcrutils.path import pyrootdir

	assert pyrootdir() == p.Path()


def test_nextname():
	from tcrutils.path import nextname

	assert nextname("a") == "a (1)"
	assert nextname("a (1)") == "a (2)"
	assert nextname("a.txt") == "a.txt (1)"
	assert nextname("a.txt (1)") == "a.txt (2)"


def test_nextname_file_ext_fix():
	from tcrutils.path import nextname_file_ext_fix

	assert nextname_file_ext_fix("a") == "a (1)"
	assert nextname_file_ext_fix("a (1)") == "a (2)"
	assert nextname_file_ext_fix("a.txt") == "a (1).txt"
	assert nextname_file_ext_fix("a (1).txt") == "a (2).txt"


@pytest.mark.parametrize(
	("path", "reserved", "strict_dictset"),
	(
		("nya", False, {}),
		("nya.", True, {}),
		("nya ", True, {}),
		(" nya", False, {}),
		(" nya", True, {True}),
		(" ", True, {}),
		("PRN", True, {}),
		("PORN", False, {}),
	),
)
def test_isreserved(path, reserved, strict_dictset):
	strict = True in strict_dictset

	from tcrutils.path import isreserved

	assert isreserved(path, strict=strict) == reserved
