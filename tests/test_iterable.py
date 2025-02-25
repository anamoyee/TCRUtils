def test_batched():
	from tcrutils.iterable import batched

	assert batched("1234567890", n=3) == ["123", "456", "789", "0"]
	assert batched("1234567890", n=3, back_to_front=True) == ["1", "234", "567", "890"]
	assert batched("", n=3) == []


def test_cut_at():
	from tcrutils.iterable import cut_at

	assert cut_at("uwuwuwuwuwu", n=10) == "uwuwuwu..."
	assert cut_at("uwuwuwuwuw", n=10) == "uwuwuwuwuw"
	assert cut_at("https://google.com/path", n=100, shrink_links_visually_if_fits=True) == "[https:/google.com/](<https://google.com/path>)"
	assert cut_at("https://google.com/path", n=20, shrink_links_visually_if_fits=True) == "https://google.co..."
