import contextlib
import random


@contextlib.contextmanager
def random_seed_lock(seed):
	rng = random.Random(seed)
	yield rng
