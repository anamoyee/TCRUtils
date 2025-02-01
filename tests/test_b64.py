from tcrutils.b64 import decode, encode


def test_b64e():
	assert encode("nyaa~!!") == "bnlhYX4hIQ=="


def test_b64d():
	assert decode("bnlhYX4hIQ==") == "nyaa~!!"
