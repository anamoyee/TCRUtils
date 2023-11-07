# fmt: off
if __import__('sys').version_info[:2] != (3, 11):
  msg = 'Use py311'
  raise RuntimeError(msg)

if True:  # \/ # Imports
  import time

  import tcrutils as tcr
  from tcrutils import *

console.debug(sorted([x for x in globals() if not x.startswith('_')]))

if True:  # \/ # Tests

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
    console(list(dict_zip({'a': 1}, {'a': 1})), recursive=False)
    console(1, 2, 3)
    console(
      list(dict_zip({'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 5, 'c': 6})),
      recursive=False,
    )

  def test_oddeven():
    console(f'{tcr.oddeven("1") = }')
    console(f'{tcr.oddeven("2") = }')
    console(f'{tcr.oddeven( 3 ) = }')
    console(f'{tcr.oddeven( 4 ) = }')

  @tcr.timeit(printhook=console)
  def test_timeit():
    times = 3
    for i in range(times):
      tcr.timeit.start(f'stuff{i+1}')
      print(f'doing some stuff... (#{i+1})')
      time.sleep(0.2)
      tcr.timeit.stop(f'stuff{i+1}', printhook=console)

  def test_autorun():
    @tcr.autorun
    def _test_autorun():
      console('Autoran')

  def test_breakpoint():
    tcr.breakpoint()
    tcr.breakpoint('asdf')
    tcr.breakpoint(clear=False)
    tcr.breakpoint(printhook=print)

  def test_getch():
    print(tcr.getch())

  @trei(ZeroDivisionError, excepth=print)
  def test_trei():
    1 / 0  # noqa: B018

  def test_asert():
    asert(lambda: 1 == 1)
    asert(lambda: 1 == 2)

  def test_iterable():
    console(tcr.batched('1234567890', n=3))
    console(repr(tcr.cut_at("uwuwuwuuwuwu", n=10)))
    console(repr(tcr.cut_at("uwuwuwuuwuwu", n=4)))
    console(repr(tcr.cut_at("uwuwuwuuwuwu", n=3)))
    console(repr(tcr.cut_at("uwuwuwuuwuwu", n=2)))
    console(repr(tcr.cut_at("uwuwuwuuwuwu", n=1)))
    console(repr(tcr.cut_at("uwuwuwuuwuwu", n=0)))
    console(repr(tcr.cut_at("uwuwuwuuwuwu", n=-1)))
    console(((a := tcr.cut_at("http://te.st.com.chudj/asdf", n=16, filter_links=r"[\3]")), len(a)), print_iterable_=False)
    console(((a := tcr.cut_at("http://te.st/asdf", n=16, filter_links=False)), len(a)), print_iterable_=False)
    console(((a := tcr.cut_at("uwuwuwuuwuwuieiei", n=16, filter_links=r"[\3]")), len(a)), print_iterable_=False)


if True:  # \/ # Test setup
  for k, v in globals().copy().items():  # Decorate each test_... function with the @test decorator
    if k.startswith('test_'):
      globals()[k] = tcr.test(v)

if __name__ == '__main__':
  # test_timestr()
  # test_dict_merge()
  # test_dict_zip()
  # test_oddeven()
  # test_timeit()
  # test_autorun()
  # test_breakpoint()
  # test_getch()
  # test_trei()
  # test_asert()
  # test_iterable()
  pass  # noqa: PIE790, RUF100
