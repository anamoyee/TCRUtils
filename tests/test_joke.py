def test_echo():
	from tcrutils.joke import echo

	assert (echo.nya) == ("nya")
	assert (echo[::]) == (slice(None, None, None))
	assert (echo ^ 3) == (3)
