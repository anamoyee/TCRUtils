# fmt: off
#if __import__('sys').version_info[:2] != (3, 12):
#  __import__('os').system(r'"C:\Users\TheCreatorrrr\AppData\Local\Programs\Python\Python312\python.exe" test.py')
#  exit()

import sys

if '--syntax-only' in sys.argv:
  import tcrutils as tcr
  tcr.console.log(f"Syntax test passed on Python %s.%s" % sys.version_info[:2])
  exit(0)

if True:  # \/ # Imports
  import asyncio
  import os
  import pathlib as p
  import time
  from typing import Any
  from typing import TypedDict as TD

  import arc
  import hikari
  import miru

  import tcrutils as tcr
  from tcrutils import asshole, c, console, rashole
  from tcrutils.src.tcr_constants import *

  # from tcrutils import *
  # from tcrutils import asshole, raises, rashole
  # from tcrutils import console as c
  # from tcrutils.discord import Permission as Perm
  # from tcrutils.discord import get_token
  # from tcrutils.discord import permissions as perms


# _rich_traceback_install(width=tcr.terminal.width-1)
if sys.gettrace() is None:
  c(sorted(_ := list(filter(lambda x: not x.startswith('_'), globals().copy()))), len(_)); del _
  c.log(f"Running on Python %s.%s" % sys.version_info[:2])


BOT: hikari.GatewayBot | None = None
ACL: arc.GatewayClient | None = None
MCL: miru.Client | None = None
def spin_up_bot(*, bot_kwargs: dict[str, Any] = {}, acl_kwargs: dict[str, Any] = {}) -> None:  # noqa: B006
  global BOT
  global ACL
  global MCL
  if BOT is not None:
    return # Already spun up
  BOT = hikari.GatewayBot(token=tcr.get_token('TESTBOT_TOKEN.txt'), intents=hikari.Intents.ALL, **bot_kwargs)
  ACL = arc.GatewayClient(BOT, **acl_kwargs)
  MCL = miru.Client(BOT)

if True:  # \/ # Tests

  def test_timestr():
    from tcrutils import timestr
    console(a := timestr.to_int('1rev'))
    console(timestr.to_str(a))
    console(timestr.to_datestr(a))

  def test_dict_merge():
    from tcrutils import merge_dicts
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
    from tcrutils import dict_zip
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
    tcr.breakpoint('uwu', 'owo', '^w^')
    tcr.breakpoint(clear=False)
    tcr.breakpoint(printhook=print)

  def test_getch():
    print(tcr.getch())

  def test_trei():
    from tcrutils import trei

    @trei(ZeroDivisionError, excepth=print)
    def inner():
      1 / 0  # noqa: B018

    inner()

  def test_asert():
    from tcrutils import asert
    asert(lambda: 1 == 1)
    asert(lambda: 1 != 2)

  def test_iterable(*, batched_=True, cut_at_=True):
    if batched_:
      console(tcr.batched('1234567890', n=3), print_iterable_=False)
      console(tcr.batched('1234567890', n=3, back_to_front=True), print_iterable_=False)
      console(tcr.batched('', n=3), print_iterable_=False)
      console(tcr.batched('', n=3) or [[]], print_iterable_=False)
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
  def test_print_iterable(print_iterable=tcr.print_iterable, **kwargs):
    import datetime as dt

    from tcrutils import Null
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

    class Client:
      test: str

      def __init__(self, test: str) -> None:
        self.test = test

      def __repr__(self) -> str:
        return f'{self.__class__.__name__}(test={self.test!r})'

    print_iterable(Client('test'), **kwargs)
    print_iterable(0x7FFFFFFF, **kwargs)
    print_iterable(tcr.types.HexInt(0x7FFFFFFF), **kwargs)
    print_iterable(float | int, **kwargs)
    print_iterable(str, **kwargs)
    print_iterable([[[[[[[[[[[[]]]]]]]]]]]], **{**kwargs, "let_no_indent": False})
    print_iterable([tcr.types.QuotelessString("quoteless string")]*3, **kwargs)
    print_iterable({
      "a": [
        'nya', 'owo', 'uwu', {
          "12": 34,
          '56': 78,
        },
        [10, 20, 30],
      ]
    }, **kwargs)
    print_iterable({
      "b": [],
    }, **kwargs)
    print_iterable({
      "b": 2,
    }, **kwargs)
    print_iterable({
      "b": 2,
      "d": 4,
    }, **kwargs)
    print_iterable({
      "b": None,
    }, **kwargs)
    print_iterable({
      "b": Null,
    }, **kwargs)

    datetime = dt.datetime.now()
    print_iterable(datetime, **kwargs)
    print_iterable(datetime.date(), **kwargs)
    print_iterable(datetime.time(), **kwargs)


    ts = tcr.types.UnixTimestampInt(1719949074443)

    print_iterable(ts, **kwargs, _raise_errors=True)
    print_iterable(ts.to_datetime(), **kwargs, _raise_errors=True)

  def test_markdown():
    from tcrutils import codeblock, uncodeblock
    console.debug(codeblock("asdf"))
    console.debug(codeblock("uwu", langcode='owo'))
    console.debug(codeblock(""))
    console.debug([a := codeblock("asxxxxxxxxxdf", langcode='py', max_length=17), len(a)])
    console.debug(uncodeblock(codeblock("hihi", langcode='py')))
    console.debug(uncodeblock("```py\n:3```"))

  def test_extract_error():
    from tcrutils import extract_error
    console(extract_error(ValueError('asdf')))
    console(extract_error(ValueError('uwu')))
    console(extract_error(ValueError()))
    console(extract_error(ValueError))
    console(extract_error(ValueError("Ewwow~!"), raw=True), print_iterable_=False)

  def test_fizzbuzz(n=30):
    console({x+1: tcr.fizzbuzz(x+1) for x in range(n)})

  def test_constants():
    from tcrutils.discord import DiscordLimits
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
    @tcr.timeit
    def bogo_sort():
      console(tcr.bogo_sort(tcr.shuffled(list(range(5))*2)))

    @tcr.timeit
    def stalin_sort():
      console(tcr.stalin_sort(tcr.shuffled(list(range(100))*2)))

    bogo_sort()
    stalin_sort()

  def test_print_block():
    from tcrutils import print_block
    print_block('Test')
    print_block('OwO', '#', margin=1, border=10, padding=2)
    console(print_block('UwU', raw=True, padding_top=2), print_iterable_=False)

  def test_dir():
    from tcrutils import dir2, dir3
    console(dir(console))
    console(dir2(console))
    console(dir3(console))

  def test_nth():
    console({x: tcr.nth(x) for x in range(-24, 25)})

  def test_timestr_plsh_weekdays():
    from tcrutils import timestr
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
    from tcrutils.discord import DiscordLimits
    from tcrutils.discord import Permission as Perm
    from tcrutils.discord import permissions as perms
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
    asshole(tcr.able(int, 'ff8000', base=16), (True, 16744448), expr='tuple(a) == b')
    asshole(tcr.able(int, 'ff8000'), expr='not a')

  def test_insist():
    from functools import partial

    from tcrutils import insist
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
    class Database(tcr.ShelveDB):
      directory = str((p.Path(__file__).parent / 'test_db').absolute())

      defaults = {
        "r": list,
      }

    c(Database.exists('1'))
    c(Database.exists('0'))

    db1 = Database("test145345")
    # db2 = Database("test2")
    # db3 = Database("test3")

    c(db1)

    # db1.clear()

    # c(db1)

    # c(db1['r'])

    # c(db1)

    # c(db1.get_directory())

    # db['OwO'] = 'UwU'
    # console(db)

    # del db['OwO']
    # console(db)

    # db.setdefault("a", "A")
    # console(db)
    # db.setdefault("b", "B")
    # db.setdefault("c", "C")
    # db.setdefault("d", "D")
    # console(db)

    # console(db.pop('a'))
    # console(db)
    # console(db.popitem())
    # console(db)
    # console(db.popitem())
    # console(db)
    # console(db.popitem())
    # console(db)

  def test_fmt_iterable(*, printhook=print, syntax_highlighting=True, **kwargs):
    kwargs['syntax_highlighting'] = syntax_highlighting
    from arc import GatewayContext

    printhook(tcr.fmt_iterable(GatewayContext, **kwargs))

    a = []
    a.append(a)

    printhook(tcr.fmt_iterable(a, **kwargs))

  def test_getattr_queue():
    print(test_getattr_queue())

  def test_language():
    from tcrutils import apostrophe_s, make_plural
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
    from tcrutils import float2int
    console(float2int(10.2))
    console(float2int(10))

  def test_manyattrs():
    from tcrutils import getmanyattrs, hasmanyattrs
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
    from tcrutils import raises
    asshole(raises((lambda x: 1 / x), x=1)(ZeroDivisionError), False)
    asshole(raises((lambda x: 1 / x), x=0)(ZeroDivisionError), True)

  def test_asshole():
    asshole("Expected pass", "Expected pass")
    asshole(2137, 69, suppress=True)
    asshole(1, 2, expr="a < b")
    asshole('1', expr=int)
    asshole([1], expr=bool)
    asshole([], expr=bool, suppress=True)
    asshole([], expr=list, suppress=True)

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
    from tcrutils import extract_error
    console(extract_error(BaseException))
    console(extract_error(Exception))
    console(extract_error(BaseException("Message")))
    console(extract_error(Exception("Message")))
    console(extract_error(BaseExceptionGroup))
    console(extract_error(ExceptionGroup))
    console(extract_error(BaseExceptionGroup("Message", (Exception(),))))
    console(extract_error(ExceptionGroup("Message", (Exception(),))))

  def test_warning_catcher():
    tcr.WarningCatcher()
    async def a():
      ...
    a()

  def test_error_catcher():
    tcr.ErrorCatcher()
    # import rich.traceback
    # rich.traceback.install()

    raise ValueError("err")

  def test_console_new():
    console('test')
    console.log('test')
    console.error('test')
    console.warn('test')
    console.critical('test')

  def test_dunder_version():
    console({
      '__version__': tcr.__version__,
      '__name__': tcr.__name__,
      '__file__': tcr.__file__,
    })

  def test_dotdicts():
    from tcrutils import Undefined
    dd = tcr.DotDict({"a": 1, "b": 2})
    asshole(dd.a, 1)
    asshole(dd.b, 2)
    rashole(lambda: dd.c)(KeyError)
    del dd.a
    asshole(dd, {"b": 2})


    dd = tcr.DotDict({"a": 1, "b": {"c": 3}})
    asshole(dd.b.c, 3)

    jsd = tcr.JSDict({"a": 1, "b": 2})
    asshole(jsd['a'], 1)
    asshole(jsd['b'], 2)
    asshole(jsd['c'], Undefined)

    jsdd = tcr.JSDotDict({"a": 1, "b": 2})
    asshole(jsdd.a, 1)
    asshole(jsdd.b, 2)
    asshole(jsdd.c | 3, 3)
    del jsdd.asdfa # Nothing should happen because jsdict will suppress the invalid item - because javascript

  def test_null():
    from tcrutils import Null, Undefined
    console(Null)
    console(Undefined)
    asshole(Null is Null.__class__())
    asshole(Undefined is Undefined.__class__())
    asshole(Undefined is not Null)
    console(type(Null))
    console(type(Undefined))
    console(str(Null))
    console(repr(Null))
    console(str(Undefined))
    console(repr(Undefined))
    asshole(Null | 0, 0)
    asshole(Null | 1, 1)
    asshole(0 | Null, 0)
    asshole(1 | Null, 1)
    asshole(Undefined | 0, 0)
    asshole(Undefined | 1, 1)
    asshole(0 | Undefined, 0)
    asshole(1 | Undefined, 1)
    console(Null | Undefined)
    console(Undefined | Null)
    console(Undefined | Undefined)
    console(Null | Null)

  def test_get_caller_line_number():
    console(tcr.get_lineno())
    console(tcr.get_file_colon_lineno())
    console(tcr.get_file_colon_lineno(additional_offset=10))

  def test_diff():
    console({
      1: 2,
      3: 2,
      5: 6,
    }, diff=True)
    console({
      1: 2,
      3: 4,
      5: 6,
    }, diff=True)
    console({
      1: 4,
      3: 4,
      6: 4,
      7: 4,
      5: 6,
    }, diff=True)

  async def test_execute():
    execute = tcr.Execute(placeholders={
      'uwu': lambda *_, **__: 'UwU',
      'nyaaa': lambda *_, **__: 'NYAAA{}AAA ;3',
      'mirror': lambda ___, param1, *_, **__: param1[::-1],
      'mirrorUwU': lambda ___, param1, *_, **__: param1[::-1] + 'hihi',
    })

    console(await execute("asdfasdfgsdfg {uwu} {nyaaa} {mirror{uwu}|2345}"))

  def test_divstring():
    s = tcr.SlashableString("uwu")

    a = s / s / s

    console.debug(a)

  def test_cint():
    i: int = tcr.CInt(11)

    c(i)
    ++i; # noqa
    c(i)

    print()

    c(i)
    -i; # noqa
    c(i)
    -i; # noqa
    c(i)

    print()

    c(--i.bit_length()) # noqa

  def test_generate_type_hinter():
    import rich
    class Example:
      def __init__(self):
        self.name = "John"
        self.age = 30
        self.is_active = True

      class InnerClass:
        def __init__(self):
          ...

      def func(self, value: int, clause: InnerClass):
        pass

      def func2(self) -> int:
        pass

      def argskwargsfunc(self, *args, **kwargs) -> int:
        pass

      def defaultfunc(self, /, value: int = 1, *, s: str | None = None) -> int:
        pass

    tcr.generate_type_hinter(Example(), print=rich.print, clipboard=False)

  def test_generate_type_hinter2():
    imgui = __import__('imgui')

    tcr.generate_type_hinter(imgui, print=True, clipboard=False)

  def test_imgui_handler():
    import imgui

    from tcrutils.imgui import ImGuiHandler, ensure_dependencies, imtypes

    imgui: imtypes.ImguiType

    ensure_dependencies()

    class State:
      time = 0.0
      frames = 0
      every = tcr.imgui.Every(30)
      last_fps = 0

    @ImGuiHandler().set_title("nyaa")
    def gui(state: State):
      with imgui.begin("nya"):
        current_time = imgui.get_time()
        delta_time = current_time - state.time

        state.time = current_time

        if State.every():
          fps = state.frames / delta_time / 30
          state.frames = 0
          state.last_fps = fps
        else:
          fps = state.last_fps
        imgui.text("FPS: %.0f" % fps)

      state.frames += 1

    gui.run(State())

  def test_b64():
    def get_enc_len(text: str, I: int):
      encoded = tcr.b64.encode(text)

      for _ in range(I):
        encoded = tcr.b64.encode(encoded)

      return len(encoded)

    c([
      get_enc_len("uwu", x) for x in range(40)
    ])

  async def test_dynamic_responses():
    EXECUTE = tcr.dynamic_responses.DynamicResponseBuilder(
      tcr.dr.placeholder_set.ALL_NON_DISCORD,
      parens=('{', '}'),
      error_on_missing_placeholder=False,
    )

    asshole.error_func = lambda *_, **__: ...

    asshole(await EXECUTE("owo {add|1|{add|2|2}} asdfasdfgsdfg {uwu} {nyaaa}"), expr='bool(a) == b')
    # This shall forever stay executed to signify a potential fuckup in the nested placeholder capabilities

    if (__TEXT := True):
      print(); c('COMMENT', quoteless=True)
      asshole(await EXECUTE("cu{comment|comment}ment"), "cument")
      asshole(await EXECUTE("#cu{#|comment}ment"), "#cument")
      asshole(await EXECUTE("//cu{//|comment}ment"), "//cument")
      print(); c('VAR', quoteless=True)
      asshole(await EXECUTE("{var|var1|nya}{var1} {var|var1}"), "nya nya")
      print(); c('TEST', quoteless=True)
      asshole(await EXECUTE("{test|a|a|T|F}F2"), "TF2")
      asshole(await EXECUTE("T{test|a|ż|F|F}2"), "TF2")
      asshole(await EXECUTE("{test|a|a}"), "true")
      asshole(await EXECUTE("{test|a|ż}"), "false")
      asshole(await EXECUTE("{test|a}"), "{test|a}")
      asshole.total(prefix='\n')

    if (__MATH := True):
      c.hr()
      print(); c('ADD', quoteless=True)
      asshole(await EXECUTE("{add}"), "0")
      asshole(await EXECUTE("{add|4}"), "4")
      asshole(await EXECUTE("{add|1|1}"), "2")
      asshole(await EXECUTE("{add|1|1|2.4}"), "4.4")
      print(); c('SUBTRACT', quoteless=True)
      asshole(await EXECUTE("{sub}"), "0")
      asshole(await EXECUTE("{sub|5}"), "5")
      asshole(await EXECUTE("{sub|1|2}"), "-1")
      asshole(await EXECUTE("{sub|1|2|3}"), "-4")
      print(); c('MULTIPLY', quoteless=True)
      asshole(await EXECUTE("{mul}"), "1")
      asshole(await EXECUTE("{mul|3|3}"), "9")
      asshole(await EXECUTE("{mul|3|3|4}"), "36")
      asshole(await EXECUTE("{mul|2|3.4}"), "6.8")
      print(); c('DIVIDE', quoteless=True)
      asshole(await EXECUTE("{div}"), "1")
      asshole(await EXECUTE("{div|3}"), "3")
      asshole(await EXECUTE("{div|1|2}"), "0.5")
      asshole(await EXECUTE("{div|15|3|5}"), "1")
      print(); c('FLOOR DIVIDE', quoteless=True)
      asshole(await EXECUTE("{floordiv}"), "1")
      asshole(await EXECUTE("{fdiv|3}"), "3")
      asshole(await EXECUTE("{fdiv|1|2}"), "0")
      asshole(await EXECUTE("{fdiv|34|3}"), "11")
      print(); c('POWER', quoteless=True)
      asshole(await EXECUTE("{pow}"), "{pow}")
      asshole(await EXECUTE("{pow|3}"), "9")
      asshole(await EXECUTE("{pow|2|3}"), "8")
      asshole(await EXECUTE("{pow|2|2|2|2}"), "256")
      print(); c('MOD', quoteless=True)
      asshole(await EXECUTE("{mod}"), "{mod}")
      asshole(await EXECUTE("{mod|5}"), "5")
      asshole(await EXECUTE("{mod|15|3}"), "0")
      asshole(await EXECUTE("{mod|15|2|3}"), "1")
      print(); c('ROUND', quoteless=True)
      asshole(await EXECUTE("{round}"), "{round}")
      asshole(await EXECUTE("{round|1.3}"), "1")
      asshole(await EXECUTE("{round|1.7}"), "2")
      asshole(await EXECUTE("{round|1.5}"), "2")
      print(); c('FLOOR', quoteless=True)
      asshole(await EXECUTE("{floor}"), "{floor}")
      asshole(await EXECUTE("{floor|6.1}"), "6")
      asshole(await EXECUTE("{floor|6.9}"), "6")
      print(); c('CEIL', quoteless=True)
      asshole(await EXECUTE("{ceil}"), "{ceil}")
      asshole(await EXECUTE("{ceil|9.1}"), "10")
      asshole(await EXECUTE("{ceil|9.9}"), "10")
      asshole.total(prefix='\n')

    if (__DEBUG := True):
      c.hr()
      c('DEBUG', quoteless=True)
      asshole.total(prefix='\n', ignore_empty=False)

  async def test_dynamic_responses_bot():
    spin_up_bot()

    EXECUTE = tcr.dynamic_responses.DynamicResponseBuilder(
      tcr.dr.placeholder_set.ALL,
      error_on_missing_placeholder=False,
      error_on_invalid_placeholder_return=False,
      context_constructors={
        "user_mentions": list,
        "role_mentions": list,
        "attachments": list,
      },
    )

    T_AUTHOR = """
## Author
Username: {username}
Globalname: {globalname}
Nickname: {nickname}
Tag: {tag}
Mention: {@}
Discrim: {discrim}
ID: {id}
Bot?: {bot}
Human?: {human}
Avatar: <{avatar}>
Roles: {roles}
In DMs?: {indms}
Color: {color}
"""[1:-1] # noqa: F841, RUF100

    T_SERVER = """
## Server
Name: {server|name}
ID: {server|id}
"""[1:-1]  # noqa: F841, RUF100

    CURRENT_TEST = T_SERVER

    @ACL.include
    @arc.slash_command(*2*["test_dynamic_responses"])
    async def cmd_test_dynamic_responses(
      ctx: arc.Context,
      text: arc.Option[str, arc.StrParams('The reminder syntax (use /help for help)')] = None,
    ) -> None:
      if text is None:
        text = CURRENT_TEST

      result = await EXECUTE(text, **{
        'ctx': ctx,
      })

      c(result.resp)

      await ctx.respond(**result.resp)

    @BOT.listen(hikari.MessageCreateEvent)
    async def on_message(event: hikari.MessageCreateEvent) -> None:
      if event.author_id == BOT.get_me().id:
        return

      if hasattr(event, 'guild_id') and event.channel_id != 1125889206586183682:
        return

      if not event.content:
        return

      result = await EXECUTE(event.content if event.content != 't' else CURRENT_TEST, **{
        'event': event,
      })

      c(result.resp)

      await event.message.respond(**result.resp)

  def test_tempfile():
    path = tcr.temp_file("Test contents")
    c(path)
    input()

  def test_skip_first_call():
    @tcr.skip_first_call
    def _printer(x):
      c(x)

    _printer(1)
    _printer(2)
    _printer(3)

  def test_ensure_deps():
    ensure_dependencies = tcr.ensure_depencencies.DependencyEnsurer(
      tcr.ensure_depencencies.Dependency(import_as='requests'),
      tcr.ensure_depencencies.Dependency(import_as='hikari'),
      tcr.ensure_depencencies.Dependency(import_as='lightbulb', pip_install_as='hikari-lightbulb'),
      tcr.ensure_depencencies.Dependency(import_as='abd', pip_install_as='abd'),
    )

    ensure_dependencies()

  def test_dpy():
    while (a := input("Escape markdown >>> ")):
      c(tcr.discord.escape_markdown(a))

    while (a := input("Remove markdown >>> ")):
      c(tcr.discord.remove_markdown(a))

    while (a := input("Escape mentions >>> ")):
      c(tcr.discord.escape_mentions(a))

  def test_random_seed_lock():
    import random

    TIMES = 10
    SEED = 42

    c(random.randint(0, 1000000) for _ in range(TIMES))
    with tcr.random_seed_lock(SEED) as rng:
      c(rng.randint(0, 1000000) for _ in range(TIMES))

  async def test_bot_shorts():
    import random as rng

    spin_up_bot()

    @BOT.listen(hikari.DMMessageCreateEvent)
    async def on_dm(event: hikari.DMMessageCreateEvent):
      if not event.is_human:
        return

      async def yes(btn: miru.Button, ctx: miru.ViewContext):
        await ctx.respond('Yes clicked')

      async def no(btn: miru.Button, ctx: miru.ViewContext):
        await ctx.respond('No clicked')

      class CustomButton(miru.Button):
        async def callback(self, ctx: miru.ViewContext):
          await ctx.respond('Custom clicked')

      class CustomSelect(miru.TextSelect):
        async def callback(self, ctx: miru.ViewContext):
          await ctx.respond('Custom selected: ' + repr(self.values[0]))

      # await tcr.discord.confirm(
      #   responder=event.message.respond,
      #   miru_client=MCL,
      #   yes_callback=yes,
      #   no_callback=no,
      #   buttons=(True, True, True, True, False, CustomButton('Custom btn'), CustomSelect(options=[miru.SelectOption(label=x) for x in ['nya', 'uwu', 'owo']])),
      #   disable_on_click=True,
      # )

      randoms = [bool(rng.randint(0, 1)) for _ in range(25)]

      await tcr.discord.confirm(
        responder=event.message.respond,
        miru_client=MCL,
        yes_callback=yes,
        no_callback=no,
        buttons=randoms,
        disable_on_click=True,
        view_kwargs={"timeout": 10},
      )

  def test_partial_class():
    @tcr.partial_class
    class Button:
      def __init__(self, label: str):
        self.label = label

      def __repr__(self):
        return f'Button(label={self.label!r})'

    class YesButton(Button, label='Yes'): ...
    class NoButton(Button, label='No'): ...

    y = YesButton()
    c(repr(y)) # -> Button(label='Yes')
    n = NoButton()
    c(repr(n)) # -> Button(label='No')
    n2 = NoButton(label='Nuh uh') # Overridden
    c(repr(n2)) # -> Button(label='Nuh uh')

  def test_with_overrides():
    from dataclasses import dataclass

    @dataclass(kw_only=True)
    class A:
      a: int
      b: str

      @tcr.with_overrides('a', 'b')
      def get_a(self, *, a: int, b: str):
        return a, b

    a = A(a=1, b='b')

    c(a.get_a())
    c(a.get_a(a=2))
    c(a.get_a(b='c'))
    c(a.get_a(a=2, b='c'))

  def test_tstr():
    import datetime as dt

    import pytz

    STRFTIME_FORMAT_SPECIFIER = "%a, %Y-%m-%d %H:%M:%S"

    tcr.timeit.start('timezone')

    tzinfo = pytz.timezone('Europe/Warsaw')

    tcr.timeit.stop('timezone')

    tstr = tcr.TStr(tzinfo=tzinfo, fix_timezone=True)

    now1 = tstr.to_datetime('0').replace(microsecond=0)
    now2 = dt.datetime.now(tz=tzinfo).replace(microsecond=0)

    console(now1.strftime(STRFTIME_FORMAT_SPECIFIER))
    console(now2.strftime(STRFTIME_FORMAT_SPECIFIER))
    asshole(now1, now2)
    asshole(now1 - now2, dt.timedelta(0))
    asshole(now1.tzinfo, now2.tzinfo)

    print(); asshole.total(); print()


    asshole(tstr.to_int('0'), 0)
    asshole(tstr.to_int('1s'), 1)
    asshole(tstr.to_int('-1h'), -3600)
    print()
    console(tstr.to_datetime('wed').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('mon').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('::').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('::!1.1.0').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('::1').strftime(STRFTIME_FORMAT_SPECIFIER)) # localhost
    print()
    console(tstr.to_datetime('10:').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('23:59:59').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('1.').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('28.').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('1d!wed').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('wed!1d').strftime(STRFTIME_FORMAT_SPECIFIER))
    print()
    console(tstr.to_datetime('1rev').strftime(STRFTIME_FORMAT_SPECIFIER))
    print()
    console(tstr.to_datetime(':').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('0:').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(tstr.to_datetime('23:59:59').strftime(STRFTIME_FORMAT_SPECIFIER))
    console('1.', tstr.to_datetime('1.').strftime(STRFTIME_FORMAT_SPECIFIER))
    console('28.', tstr.to_datetime('28.').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(f'{now1.day}.', tstr.to_datetime(f'{now1.day}.').strftime(STRFTIME_FORMAT_SPECIFIER))
    console('1.!::', tstr.to_datetime('1.!::').strftime(STRFTIME_FORMAT_SPECIFIER))
    console('28.!::', tstr.to_datetime('28.!::').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(f'{now1.day}.!::', tstr.to_datetime(f'{now1.day}.!::').strftime(STRFTIME_FORMAT_SPECIFIER))
    console('1.!14::', tstr.to_datetime('1.!14::').strftime(STRFTIME_FORMAT_SPECIFIER))
    console('28.!14::', tstr.to_datetime('28.!14::').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(f'{now1.day}.!14::', tstr.to_datetime(f'{now1.day}.!14::').strftime(STRFTIME_FORMAT_SPECIFIER))
    console(f'wed!:', tstr.to_datetime(f'wed!:').strftime(STRFTIME_FORMAT_SPECIFIER))
    print()
    console(tstr.to_str(60))
    console(tstr.to_str(100))
    console(tstr.to_str(1000))
    console(tstr.to_str(10000))
    console(tstr.to_str(100000, round_to=0))
    console(tstr.to_str(100000, round_to=1))
    console(tstr.to_str(100000, round_to=2))
    console(tstr.to_str(100000, round_to=5))
    console(tstr.to_str(100000, round_to=6))
    console(tstr.to_str(100000, round_to=8))
    console(tstr.to_str(100000, round_to=100))
    print()
    console(tstr.to_str2(100))
    console(tstr.to_str2(1000))
    console(tstr.to_str2(100, always_show_days=True))
    console(tstr.to_str2(1000, always_show_days=True))
    console(tstr.to_str2(10000))
    console(tstr.to_str2(100000))
    print()
    console(tstr.to_strf(60))
    console(tstr.to_strf(100))
    console(tstr.to_strf(1000))
    console(tstr.to_strf(10000))
    console(tstr.to_strf(100000))
    console(tstr.to_strf(1000000))
    console(tstr.to_strf(10000000))
    console(tstr.to_strf(100000000))
    console(tstr.to_strf(1000000000))
    print()
    rashole(tstr.to_int, '1')(ValueError)
    rashole(tstr.to_int, 'nya')(ValueError)
    print(); asshole.total()

  def test_default():
    class A(tcr.DefaultsGetSetAttr):
      defaults = {
        'nya': int,
      }

    a = A()

    a.uwu = 'owo'
    c(a.nya)
    c(a.uwu)
    c(tcr.dir3(a))


    print()

    class B(tcr.DefaultsGetAttr):
      defaults = {
        'nya': int,
      }

    b = B()

    b.uwu = 'owo'
    c(b.nya)
    c(b.uwu)
    c(tcr.dir3(b))


    print()

    class C(tcr.DefaultsGetSetItem):
      defaults = {
        "nya": int,
      }

    ce = C()

    ce['owo'] = 1

    c(ce['nya'])
    c(ce['owo'])
    c(ce.keys())

    print()

    class D(tcr.DefaultsGetItem):
      defaults = {
        'nya': int,
      }

    d = D()

    d['owo'] = 1

    c(d['nya'])
    c(d['owo'])
    c(d.keys())

  def test_cached_instances_meta():
    # class A(metaclass=tcr.CachedInstancesMeta, max_instances=2, max_time=2, restore_method="restore"):
    #   def __init__(self, a, b, *, c):
    #     self.a = a
    #     self.b = b
    #     self.c = c

    #   def restore(self):
    #     c('restoring', self)

    # print(1)
    # a1 = A(1, 2, c=1)
    # print(2)
    # a2 = A(1, 2, c=1)
    # print(3)
    # a3 = A(1, 2, c=1)
    # print(4)

    # c(a1 is a2 and a2 is a3)
    # c(a1._cache)

    class TestCIM_DB(tcr.ShelveDB, metaclass=tcr.CachedInstancesMeta, max_instances=2, max_time=2, restore_method="restore"):
      directory = str((p.Path(__file__).parent / 'test_db').absolute())

    db = TestCIM_DB("tedddst145345")

    c(db.iter_all_path_names())

    c(db)
    db.close()
    db['asdf'] = 1
    c(db['asdf'])
    c(db)
    db.restore()
    c(db)

  def test_gmail():
    from tcrutils.src.tcr_joke import gmail

    my_email = "my_email"@gmail.com

    my_email.send(title="Tytuł emaila", body="treść maila")

    # print(my_email)
    # print("my_email"@gmail.org)
    # print("my_email"@gmail.co.uk)

  def test_dir_recursive():
    class A(dict):
      def test(self):
        return 'nya'

      a = 1

    a = A()

    a.b = 'b'

    c(tcr.vars2(a, vars=tcr.vars_recursive))

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
    print_iterable=tcr.print_iterable,
    syntax_highlighting=1,
    # let_no_indent=0,
    # force_no_indent=0,
    # force_no_spaces=0,
    # force_complex_parenthesis=1,
    # item_limit=10,
    # # let_no_inder_max_non_iterables=10,
    # # let_no_inder_max_iterables=10,
    # prefer_full_names=1,
    # force_union_parenthesis=1,
    # depth_limit=3,
  )
  # test_print_iterable(print_iterable=print_iterable, syntax_highlighting=1)
  # test_print_iterable(print_iterable=lambda *args, **kwargs: print(tcr.fmt_iterable(*args, **kwargs)), syntax_highlighting=True)
  # test_print_iterable(print_iterable=print_iterable, syntax_highlighting=False)
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
  # test_extract_error2()
  # test_warning_catcher()
  # test_error_catcher()
  # test_console_new()
  # test_dunder_version()
  # test_null()
  # test_dotdicts()
  # test_get_caller_line_number()
  # test_diff()
  # asyncio.run(test_execute())
  # test_divstring()
  # test_cint()
  # test_generate_type_hinter()
  # test_generate_type_hinter2()
  # test_imgui_handler()
  # test_b64()
  # asyncio.run(test_dynamic_responses())
  # asyncio.run(test_dynamic_responses_bot())
  # test_tempfile()
  # test_skip_first_call()
  # test_ensure_deps()
  # test_dpy()
  # test_random_seed_lock()
  # asyncio.run(test_bot_shorts())
  # test_partial_class()
  # test_with_overrides()
  # test_tstr()
  # test_default()
  # test_cached_instances_meta()
  # test_gmail()
  # test_dir_recursive()
  # test_fmt_iterable()

  asshole.total(prefix='\n')
  pass  # noqa: PIE790, RUF100

if BOT:
  BOT.run()
