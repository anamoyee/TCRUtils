# fmt: off
#if __import__('sys').version_info[:2] != (3, 12):
#  __import__('os').system(r'"C:\Users\TheCreatorrrr\AppData\Local\Programs\Python\Python312\python.exe" test.py')
#  exit()


if True:  # \/ # Imports
  import os
  import pathlib as p
  import sys
  import time
  from functools import partial

  import tcrutils as tcr
  from tcrutils import *
  from tcrutils import asshole, raises, rashole
  from tcrutils.discord import Permission as Perm
  from tcrutils.discord import get_token
  from tcrutils.discord import permissions as perms

console.debug(sorted(a := [x for x in globals() if not x.startswith('_')]), len(a)); del a
console.log(f"{tcr.c}Running on Python %s.%s" % sys.version_info[:2])

if True:  # \/ # Tests

  def test_timestr():
    console(a := timestr.to_int('1rev'))
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
    result3 = merge_dicts({"first_seen": 10}, {"first_seen": 5, "data": 1}, {"first_seen": None, "data": "owo", "test": "hihi"}, strict=True)
    console(result)
    print()
    console(result2)
    print()
    console(result3)

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
    asert(lambda: 1 != 2)

  def test_iterable(*, batched_=True, cut_at_=True):
    if batched_:
      console(tcr.batched('1234567890', n=3), print_iterable_=False)
      console(tcr.batched('1234567890', n=3, back_to_front=True), print_iterable_=False)
    if cut_at_:
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
      console(((a := tcr.cut_at("http://te.st.com.chudj/asgsdfgsdfgdf", n=300, filter_links=r"[\3]", shrink_links_visually_if_fits=True)), len(a)), print_iterable_=False)

  def test_path():
    console(tcr.path.newdir('owo'))
    console(tcr.path.newdir('tcrutils'))
    console(tcr.path.center(__file__))
    console(os.getcwd())

  def test_ifys():
    @tcr.convert.boolify
    def a():
      return 1
    console.debug(f'{a()!r}')

    @tcr.convert.stringify
    def a():
      return 1
    console.debug(f'{a()!r}')

    @tcr.convert.intify
    def a():
      return '10'
    console.debug(f'{a()!r}')

    @tcr.convert.listify
    def a():
      return 'asdf'
    console.debug(f'{a()!r}')

    def testify(arg):
      return f'UwU {arg} UwU'

    @tcr.convert.anyify(testify)
    def a():
      return ':3'
    console.debug(f'{a()!r}')

  #@tcr.timeit
  def test_print_iterable(print_iterable=print_iterable, **kwargs):
    mappingproxy = (type.__dict__)
    print_iterable(mappingproxy, **kwargs)
    print_iterable("aasd", **kwargs)
    print_iterable({"a": 1, "b": "2"}, **kwargs)
    print_iterable({"a": range(3)}, **kwargs)
    print_iterable(range(1 << 1000), **kwargs)
    print_iterable((), **kwargs)
    print_iterable([], **kwargs)
    print_iterable({1, 2}, **kwargs)
    print_iterable("asdf", **kwargs)
    print_iterable([3, 4, 5, range(105)], item_limit=5, **{x: y for x, y in kwargs.items() if x != 'item_limit'})
    def a():
      while True:
        yield 1
    print_iterable(a(), item_limit=3, **{x: y for x, y in kwargs.items() if x != 'item_limit'})
    print_iterable(b'100', **kwargs)
    print_iterable(bytearray([10, 20, 30]), **kwargs)
    print_iterable(b'uwu"\'', **kwargs)
    print_iterable(bytearray([10, 20, 30]), b'abcd', 'abcd', r'\1', **kwargs)
    print_iterable((Null, None, True, False), **kwargs)
    print_iterable({Null: Null, None: None, True: True, False: False}, **kwargs)
    print_iterable(1, **kwargs)
    print_iterable(1.5, **kwargs)
    print_iterable(True, **kwargs)
    print_iterable(False, **kwargs)
    print_iterable(None, **kwargs)
    print_iterable(Null, **kwargs)
    print_iterable(set(), **kwargs)
    print_iterable({10, 20, 30}, **kwargs)
    print_iterable(frozenset({"asdf", 1, 3.2j+1}), **kwargs)
    print_iterable({10: 20, 30: 40}.keys(), **kwargs)
    print_iterable({10: 20, 30: 40}.values(), **kwargs)
    print_iterable({10: 20, 30: 40}.items(), **kwargs)
    print_iterable("s p a c e (not uk)", **kwargs)
    print_iterable((1,), **kwargs)
    print_iterable([[[[]]]], **kwargs)
    print_iterable([[[10, 20, [345234582346748673485678673, 40, "a", ()]]]], **kwargs)

    class UnknownThing:
      ...

    unknown_thing = UnknownThing()
    print_iterable(unknown_thing, **kwargs)
    print_iterable(UnknownThing, **kwargs)

    ### Copied from _collections_abc.py ###
    bytes_iterator = (iter(b'asdf'))
    print_iterable(bytes_iterator, **kwargs)
    bytearray_iterator = (iter(bytearray([0xFF, 0x10])))
    print_iterable(bytearray_iterator, **kwargs)
    #callable_iterator = ???
    dict_keyiterator = (iter({"a": 1, "b": 10, "c": 100}.keys()))
    dict_valueiterator = (iter({"a": 1, "b": 10, "c": 100}.values()))
    dict_itemiterator = (iter({"a": 1, "b": 10, "c": 100}.items()))
    print_iterable(dict_keyiterator, **kwargs)
    print_iterable(dict_valueiterator, **kwargs)
    print_iterable(dict_itemiterator, **kwargs)
    list_iterator = (iter([10, 20, 30]))
    print_iterable(list_iterator, **kwargs)
    list_reverseiterator = (iter(reversed([1, 2, 3])))
    print_iterable(list_reverseiterator, **kwargs)
    range_iterator = (iter(range(3)))
    longrange_iterator = (iter(range(1 << 1000)))
    print_iterable(range_iterator, **kwargs)
    print_iterable(longrange_iterator, **kwargs)
    set_iterator = (iter({15, 25, 35}))
    print_iterable(set_iterator, **kwargs)
    str_iterator = (iter("str iterator"))
    print_iterable(str_iterator, **kwargs)
    tuple_iterator = (iter(((30, 40),)))
    print_iterable(tuple_iterator, **kwargs)
    zip_iterator = (iter(zip('abcdefg', range(3), range(4), strict=False)))
    print_iterable(zip_iterator, **kwargs)

    ## misc ##
    generator = ((lambda: (yield))())
    print_iterable(generator, **kwargs)
    print_iterable(range(0), **kwargs)

    ## coroutine ##
    async def _coro(): pass
    _coro = _coro()
    coroutine = (_coro)
    print_iterable(coroutine, **kwargs)
    _coro.close()  # Prevent ResourceWarning
    del _coro
    ## asynchronous generator ##
    async def _ag(): yield
    _ag = _ag()
    async_generator = (_ag)
    print_iterable(async_generator, **kwargs)
    del _ag
    print_iterable(range(10), **kwargs)
    print_iterable([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l']], **kwargs)

    class PrintableObj:
      def __tcr_display__(self=None, **_) -> str:
        return 'tcr.fmt-able object' + ('\'s instance' if self is not None else '')

    print_iterable([PrintableObj], **kwargs)
    print_iterable([PrintableObj()], **kwargs)

    import hikari

    print_iterable((
      hikari.Status.ONLINE,
      hikari.Status.IDLE,
      hikari.Status.DO_NOT_DISTURB,
      hikari.Status.OFFLINE,
    ), **kwargs)

    class PrintableObj2:
      value: int = -1

      def __init__(self, value: int) -> None:
        self.value = value

      def __tcr_display__(self=None, **kwargs) -> str:
        return tcr.fmt_iterable(
          tcr.clean_dunder_dict((self if self is not None else PrintableObj2).__dict__),
          _force_next_type=PrintableObj2,
          _i_am_class=not self,
          **kwargs,
        )

    print_iterable(PrintableObj2, **kwargs)
    print_iterable(PrintableObj2(69), **kwargs)
    print_iterable(tcr.discord.Snowflake(1234), **kwargs)
    print_iterable([tcr.types.QuotelessString("quoteless string")]*3, **kwargs)

  def test_color():
    printc(c("Red") + "UwU")
    printc(c("!Red") + "UwU")
    printc(c("!Red", "Yellow") + "UwU")

  def test_markdown():
    console.debug(codeblock("asdf"))
    console.debug(codeblock("uwu", langcode='owo'))
    console.debug(codeblock(""))
    console.debug([a := codeblock("asxxxxxxxxxdf", langcode='py', max_length=17), len(a)])
    console.debug(uncodeblock(codeblock("hihi", langcode='py')))
    console.debug(uncodeblock("```py\n:3```"))

  def test_extract_error():
    console(extract_error(ValueError('asdf')))
    console(extract_error(ValueError('uwu')))
    console(extract_error(ValueError()))
    console(extract_error(ValueError))
    console(extract_error(ValueError("Ewwow~!"), raw=True), print_iterable_=False)

  def test_fizzbuzz(n=30):
    console({x+1: tcr.fizzbuzz(x+1) for x in range(n)})

  def test_constants():
    console(x for x in [
      BACKSLASH,
      NEWLINE,
      CARR_RET,
      BACKSPACE,
      BACKTICK, BACKTICKS,
      APOSTROPHE, QUOTE,
      FAKE_PIPE,
      DiscordLimits,
    ])

  def test_sort():
    @autorun
    @tcr.timeit
    def bogo_test():
      console(tcr.bogo_sort(tcr.shuffled(list(range(5))*2)))
    @autorun
    @tcr.timeit
    def stalin_sort():
      console(tcr.stalin_sort(tcr.shuffled(list(range(100))*2)))

  def test_print_block():
    print_block('Test')
    print_block('OwO', '#', margin=1, border=10, padding=2)
    console(print_block('UwU', raw=True, padding_top=2), print_iterable_=False)

  def test_dir():
    console(dir(console))
    console(dir2(console))
    console(dir3(console))

  def test_nth():
    console({x: tcr.nth(x) for x in range(-24, 25)})

  def test_timestr_plsh_weekdays():
    console(
      a := timestr.to_int("poniedzialek"),
    )

    console(
      timestr.to_datestr(a)
    )

  def test_console_or_ror():
    print(console | "UwU")
    print("UwU" | console)

  def test_christmas_tree():
    # print(tcr.christmas_tree())
    print(tcr.christmas_tree(symbol="C#"))
    # print(tcr.christmas_tree(symbol="C+", height=3))

  def test_recursive_sum():
    console(tcr.recursive_sum([1, 2, 3, 4, [99, 4, 5]]))

  def test_discord():
    console(DiscordLimits)
    print()

    class Guild:
      owner_id = 1234

    class Author:
      id = 1234

    class Role:
      permissions = Perm.ADMINISTRATOR

    class Member(Author):
      @staticmethod
      def get_roles():
        return [Role()]

    class Message:
      member = Member()

    class Event:
      message = Message()
      author = Author()
      member = Member()

      @staticmethod
      def get_guild():
        return Guild()

    perms.devlist = [1234]

    console(perms.has_by_GMCE(Event(), Perm.ADD_REACTIONS))

    console(perms.has(
      a1 := Perm.ADMINISTRATOR,
      a2 := Perm.CHANGE_NICKNAME | Perm.ADD_REACTIONS,
      allow_administrator=True,
    ))
    console(perms.to_str(a1))
    console(perms.to_str(a2))

  def test_terminal():
    print(tcr.terminal.size, type(tcr.terminal.size), complex(tcr.terminal.size))

  def test_get_token():
    rashole(tcr.get_token)(FileNotFoundError)

  def test_thisdir():
    console(os.getcwd())
    console(tcr.path.thisdir(chdir=True))
    console(os.getcwd())

  def test_able():
    console(tcr.able(int, '1'))
    console(tcr.able(int, 'a'))

  def test_insist():
    from functools import partial
    number = int(insist(
      partial(input, "Input a number: "),
      partial(tcr.able, int)
    ))

    console(number)

  def test_ntpath():
    console(tcr.path.nt_validname(p.Path.cwd()))
    console(tcr.path.nt_validname(os.getcwd()))
    console(tcr.path.nt_validname("uwu:"))
    console(tcr.path.nt_validname(" uwu\n"))
    console(tcr.path.nt_validname(" uwu"))
    console(tcr.path.nt_validname(" u\rwu"))
    console(tcr.path.nt_validname(p.Path(" u\rwu")))
    console(tcr.path.nt_validname("."))
    console(tcr.path.nt_validname("."))
    console(tcr.path.nt_validname("..."))
    console(tcr.path.nt_validname(""))

  def test_newdir2():
    console(tcr.path.nextname_file_ext_fix(tcr.path.nextname_file_ext_fix()))

  def test_sdb():
    class DB(tcr.ShelveDB):
      directory = p.Path(__file__).parent / 'test_db'

    db = DB("0")
    db.clear()

    console(db)

    db['OwO'] = 'UwU'
    console(db)

    del db['OwO']
    console(db)

    db.setdefault("a", "A")
    console(db)
    db.setdefault("b", "B")
    db.setdefault("c", "C")
    db.setdefault("d", "D")
    console(db)

    console(db.pop('a'))
    console(db)
    console(db.popitem())
    console(db)
    console(db.popitem())
    console(db)
    console(db.popitem())
    console(db)

  def test_fmt_iterable(*, printhook=print, **kwargs):
    printhook(tcr.fmt_iterable(10, **kwargs))
    printhook(tcr.fmt_iterable(10.3, **kwargs))
    printhook(tcr.fmt_iterable(10.4, 10, **kwargs))
    printhook(tcr.fmt_iterable(10.5, (10, 20), **kwargs))
    printhook(tcr.fmt_iterable([
      69,
      6.9,
      "UwU",
      b"OwO",
      True,
      False,
      None,
      Null,
      [],
      (),
      {},
      set(),
    ], **{**kwargs, "item_limit": 100}))
    printhook(tcr.fmt_iterable({
      "uwu": 1,
      "owo": "^w^",
    }, **kwargs))

    def generator():
      while True:
        yield 1
    printhook(tcr.fmt_iterable(range(6), **kwargs))
    printhook(tcr.fmt_iterable(generator(), **kwargs))
    printhook(tcr.fmt_iterable({Null: Null, None: None, True: True, False: False}, **kwargs))
    printhook(tcr.fmt_iterable(bytearray([0x10, 0x2A, 0x3D]), **kwargs))

  def test_getattr_queue():
    print(test_getattr_queue())

  def test_language():
    console((a := "Michael"), make_plural(a))
    console((a := "Box"), make_plural(a))
    console((a := "Bench"), make_plural(a))
    console((a := "BenCH"), make_plural(a))
    console((a := "BENCH"), make_plural(a))
    console((a := "Wife"), make_plural(a))
    console((a := "Wolf"), make_plural(a))
    console((a := "Play"), make_plural(a))
    console((a := "Cry"), make_plural(a))
    console((a := "child"), make_plural(a))
    console((a := "Child"), make_plural(a))
    console((a := "CHILD"), make_plural(a))
    console((a := "wharf"), make_plural(a))
    console((a := "furry"), make_plural(a))
    console((a := "furry"), make_plural(a))
    print()
    console((a := "furry"), apostrophe_s(a))
    console((a := "mass"), apostrophe_s(a))

  def test_float2int():
    console(float2int(10.2))
    console(float2int(10))

  def test_manyattrs():
    class Cld:
      attr1 = {}

    cld = Cld()

    console(hasmanyattrs(cld, *"attr1.clear".split('.')))
    console(getmanyattrs(cld, *"attr1.clear".split('.')))

  def test_alert():
    tcr.alert("Running in testmode")
    tcr.alert("Running in testmode", printhook=console.log)

  def test_uptime():
    uptime = tcr.Uptime()
    console(str(uptime))
    console(int(uptime))

    [sum(range(1000)) for _ in range(3000)]

    console(str(uptime))
    console(int(uptime))

  def test_clean_dunder_dict():
    console(tcr.clean_dunder_dict({
      "UwU": "OwO",
      "__UwU__": "__OwO__",
      "__UwU": "__OwO",
      "_UwU": "_OwO",
    }, strategy=2))

  def test_class():
    class SingleTuple(tcr.Singleton, tuple):
      ...

    tup = SingleTuple(('tup1',))
    tup2 = SingleTuple(('tup2',))

    console(tup)  # -> ('tup1',)
    console(tup2) # -> ('tup1',)

  def test_overload():
    class A(tcr.Overload):
      @tcr.overload
      def f(self, arg1: int):
        console('1-arg f:', arg1)

      @tcr.overload
      def f(self, arg1: int, arg2: int):  # noqa: F811
        console('2-arg f:', arg1, arg2)

      @tcr.overload
      def f(self, arg1: str):  # noqa: F811
        console('str-arg f:', arg1)

    a = A()

    a.f(10)
    a.f(20, 30)
    a.f('')

  def test_raises():
    asshole(raises((lambda x: 1 / x), x=1)(ZeroDivisionError), False)
    asshole(raises((lambda x: 1 / x), x=0)(ZeroDivisionError), True)

  def test_asshole():
    asshole("Expected pass", "Expected pass")
    asshole("Expected fail (suppressed)", 69, suppress=True)
    asshole(1, 2, expr=" a < b")

  def test_discord_ifys():
    rashole(tcr.discord.IFYs.userify, -1)(ValueError)
    asshole(tcr.discord.IFYs.userify(1 << 63), f"<@{1 << 63}>")
    rashole(tcr.discord.IFYs.userify, 1 << 63 + 1)(ValueError)
    asshole(tcr.discord.IFYs.userify(1234), '<@1234>')
    asshole(tcr.discord.IFYs.userbangify(1234), '<@!1234>')
    asshole(tcr.discord.IFYs.channelify(1234), '<#1234>')
    asshole(tcr.discord.IFYs.commandify('cmd', 1234), '</cmd:1234>')
    asshole(tcr.discord.IFYs.emojify('emo', 1234), '<:emo:1234>')
    asshole(tcr.discord.IFYs.emojify('uwu', 69, animated=True), '<a:uwu:69>')
    asshole(tcr.discord.IFYs.timeify(1), '<t:1>')
    asshole(tcr.discord.IFYs.timeify(1, 'F'), '<t:1:F>')
    rashole(tcr.discord.IFYs.timeify, 1, 'r')(ValueError)
    asshole(tcr.discord.IFYs.timeify(1, 'F'), '<t:1:F>')

  def test_extract_error2():
    console(extract_error(BaseException))
    console(extract_error(Exception))
    console(extract_error(BaseException("Message")))
    console(extract_error(Exception("Message")))
    console(extract_error(BaseExceptionGroup))
    console(extract_error(ExceptionGroup))
    console(extract_error(BaseExceptionGroup("Message", (Exception(),))))
    console(extract_error(ExceptionGroup("Message", (Exception(),))))

if True:  # \/ # Test setup
  for k, v in globals().copy().items():  # Decorate each test_... function with the @tcr.test decorator
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
  # test_iterable(batched_=True, cut_at_=False)
  # test_path()
  # test_ifys()
  test_print_iterable(
    print_iterable=print_iterable,
    syntax_highlighting=1,
    # let_no_indent=0,
    # force_no_indent=0,
    # force_no_spaces=0,
    # force_complex_parenthesis=1,
    # item_limit=10,
    # # let_no_inder_max_non_iterables=10,
    # # let_no_inder_max_iterables=10,
    # prefer_full_names=1,
  )
  # test_print_iterable(print_iterable=print_iterable, syntax_highlighting=1)
  # test_print_iterable(print_iterable=lambda *args, **kwargs: print(tcr.fmt_iterable(*args, **kwargs)), syntax_highlighting=True)
  # test_print_iterable(print_iterable=print_iterable, syntax_highlighting=False)
  # test_color()
  # test_markdown()
  # test_extract_error()
  # test_fizzbuzz()
  # test_constants()
  # test_sort()
  # test_path()
  # test_print_block()
  # test_dir()
  # test_nth()
  # test_timestr_plsh_weekdays()
  # test_console_or_ror()
  # test_christmas_tree()
  # test_discord()
  # test_terminal()
  # test_recursive_sum()
  # test_get_token()
  # test_thisdir()
  # test_able()
  # test_insist()
  # test_ntpath()
  # test_newdir2()
  # test_sdb()
  # test_language()
  # test_float2int()
  # test_manyattrs()
  # test_alert()
  # test_uptime()
  # test_clean_dunder_dict()
  # test_class()
  # test_overload()
  # test_discord_ifys()
  # test_asshole()
  # test_raises()
  test_extract_error2()
  pass  # noqa: PIE790, RUF100
