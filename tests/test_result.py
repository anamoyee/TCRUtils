import pytest
from tcrutils.result import Result, ResultUnwrappedErrOnValueError, ResultUnwrappedOnErrorError


def f(lhs: int, rhs: int) -> Result[float, ZeroDivisionError]:
	try:
		return Result.new_ok(lhs / rhs)
	except ZeroDivisionError as e:
		return Result.new_err(e)


@pytest.fixture
def good():
	return f(1, 2)


@pytest.fixture
def bad():
	return f(1, 0)


def test_good_is_ok(good):
	assert good.is_ok


def test_bad_is_err(bad):
	assert bad.is_err


def test_good_raises(good):
	with pytest.raises(ResultUnwrappedErrOnValueError):
		good.unwrap_err()


def test_bad_raises(bad):
	with pytest.raises(ResultUnwrappedOnErrorError):
		bad.unwrap()


def test_good_unwrap(good):
	assert isinstance(good.unwrap(), float)


def test_bad_unwrap(bad):
	assert isinstance(bad.unwrap_err(), ZeroDivisionError)


def test_unwrap_or(good, bad):
	X = object()
	assert good.unwrap_or(X) is not X
	assert bad.unwrap_or(X) is X


def test_unwrap_or_else(good, bad):
	X = object()
	assert good.unwrap_or_else(lambda _: X) is not X
	assert bad.unwrap_or_else(lambda _: X) is X


def test_unwrap_err_or(good, bad):
	X = object()
	assert good.unwrap_err_or(X) is X
	assert bad.unwrap_err_or(X) is not X


def test_unwrap_err_or_else(good, bad):
	X = object()
	assert good.unwrap_err_or_else(lambda _: X) is X
	assert bad.unwrap_err_or_else(lambda _: X) is not X
