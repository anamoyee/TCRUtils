import pytest


def test_echo():
	from tcrutils.joke import echo

	assert (echo.nya) == ("nya")
	assert (echo[::]) == (slice(None, None, None))
	assert (echo ^ 3) == (3)


@pytest.mark.parametrize(
	("n", "expected"),
	(
		(-30, "FizzBuzz"),
		(-29, "-29"),
		(-28, "-28"),
		(-27, "Fizz"),
		(-26, "-26"),
		(-25, "Buzz"),
		(-24, "Fizz"),
		(-23, "-23"),
		(-22, "-22"),
		(-21, "Fizz"),
		(-20, "Buzz"),
		(-19, "-19"),
		(-18, "Fizz"),
		(-17, "-17"),
		(-16, "-16"),
		(-15, "FizzBuzz"),
		(-14, "-14"),
		(-13, "-13"),
		(-12, "Fizz"),
		(-11, "-11"),
		(-10, "Buzz"),
		(-9, "Fizz"),
		(-8, "-8"),
		(-7, "-7"),
		(-6, "Fizz"),
		(-5, "Buzz"),
		(-4, "-4"),
		(-3, "Fizz"),
		(-2, "-2"),
		(-1, "-1"),
		(0, "FizzBuzz"),
		(1, "1"),
		(2, "2"),
		(3, "Fizz"),
		(4, "4"),
		(5, "Buzz"),
		(6, "Fizz"),
		(7, "7"),
		(8, "8"),
		(9, "Fizz"),
		(10, "Buzz"),
		(11, "11"),
		(12, "Fizz"),
		(13, "13"),
		(14, "14"),
		(15, "FizzBuzz"),
		(16, "16"),
		(17, "17"),
		(18, "Fizz"),
		(19, "19"),
		(20, "Buzz"),
		(21, "Fizz"),
		(22, "22"),
		(23, "23"),
		(24, "Fizz"),
		(25, "Buzz"),
		(26, "26"),
		(27, "Fizz"),
		(28, "28"),
		(29, "29"),
		(30, "FizzBuzz"),
	),
)
def test_fizzbuzz(n, expected):
	from tcrutils.joke import fizzbuzz

	assert fizzbuzz(n) == expected
