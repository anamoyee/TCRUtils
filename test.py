import time

from tcrutils import *
from tcrutils import error, oddeven, test, timeit

assert __import__('sys').version_info[:2] == (3, 11), "Use py311"

console.debug(sorted([x for x in globals() if not x.startswith('_')]))

def test_timestr():
  console(a := timestr.to_int('  3:30:30'))
  console(timestr.to_str(a))
  console(timestr.to_datestr(a))

def test_dict_merge():
  master = {
      'a': 1,
      'b': {
          'x': 2,
          'y': 3,
      },
      'd': {'asdf': 1},
  }

  slave = {
      'a': 2,
      'b': {
          'x': 6,
          'y': 4,
          'z': 5,
      },
      'c': 6,
      'd': {'sss': 1, 'asdf': None},
  }

  result = merge_dicts(master, slave, recursive=True, strict=True)
  result2 = merge_dicts({}, {}, recursive=True, strict=True)
  console(result)
  console(result2)

def test_dict_zip():
  console(list(dict_zip({"a": 1}, {"a": 1})), recursive=False)
  console(1, 2, 3)
  console(list(dict_zip({"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6})), recursive=False)

def test_oddeven():
  console(f'{oddeven("1") = }')
  console(f'{oddeven("2") = }')
  console(f'{oddeven( 3 ) = }')
  console(f'{oddeven( 4 ) = }')

@timeit(printhook=console)
def test_timeit():
  times = 3
  for i in range(times):
    timeit.start(f'stuff{i+1}')
    print(f'doing some stuff... (#{i+1})')
    time.sleep(.2)
    timeit.stop(f'stuff{i+1}', printhook=console)

for k, v in globals().copy().items(): # Decorate each test_... function with the @test decorator
  if k.startswith('test_'): globals()[k] = test(v)

if __name__ == '__main__':
  ...
  # test_timestr()
  # test_dict_merge()
  # test_dict_zip()
  # test_oddeven()
  # test_timeit()
