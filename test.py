import sys
import time

_start_time = time.perf_counter()

if True:  # \/ # Imports
	import asyncio
	import os
	import pathlib as p
	import time
	from functools import wraps
	from typing import Any
	from typing import TypedDict as TD

	import arc
	import hikari
	import miru
	import pydantic
	from tcrutils import joke
	from tcrutils import types as tcr_types
	from tcrutils.console import console
	from tcrutils.console import console as c
	from tcrutils.decorator import TimeitPartial, repeat, test, timeit
	from tcrutils.print import fmt_iterable, print_iterable
	from tcrutils.test_ import ass, rass


# _rich_traceback_install(width=tcr.terminal.width-1)
if not sys.gettrace():
	c(
		sorted(_ := list(filter(lambda x: not x.startswith("_"), globals().copy()))),
		len(_),
	)
	del _
	c.log(f"Running on Python %s.%s" % sys.version_info[:2])


BOT: hikari.GatewayBot | None = None
ACL: arc.GatewayClient | None = None
MCL: miru.Client | None = None


def spin_up_bot(
	*,
	bot_kwargs: dict[str, Any] = {},
	acl_kwargs: dict[str, Any] = {},
) -> None:
	global BOT, ACL, MCL
	if BOT is not None:
		return  # Already spun up
	BOT = hikari.GatewayBot(
		token=tcr.get_token("TESTBOT_TOKEN.txt"),
		intents=hikari.Intents.ALL,
		**bot_kwargs,
	)
	ACL = arc.GatewayClient(BOT, **acl_kwargs)
	MCL = miru.Client(BOT)


if True:  # \/ # Tests

	def test_timestr():
		from tcrutils import timestr

		console(a := timestr.to_int("1rev"))
		console(timestr.to_str(a))
		console(timestr.to_datestr(a))

	def test_dict_merge():
		from tcrutils import merge_dicts

		master = {
			"a": 1,
			"b": {
				"x": 2,
				"y": 3,
			},
			"d": {"asdf": 1},
		}

		slave = {
			"a": 2,
			"b": {
				"x": 6,
				"y": 4,
				"z": 5,
			},
			"c": 6,
			"d": {"sss": 1, "asdf": None},
		}

		result = merge_dicts(master, slave, recursive=True, strict=True)
		result2 = merge_dicts({}, {}, recursive=True, strict=True)
		result3 = merge_dicts(
			{"first_seen": 10},
			{"first_seen": 5, "data": 1},
			{"first_seen": None, "data": "owo", "test": "hihi"},
			strict=True,
		)
		console(result)
		print()
		console(result2)
		print()
		console(result3)

	def test_dict_zip():
		from tcrutils import dict_zip

		console(list(dict_zip({"a": 1}, {"a": 1})), recursive=False)
		console(1, 2, 3)
		console(
			list(dict_zip({"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6})),
			recursive=False,
		)

	@timeit(printhook=console)
	def test_timeit():
		times = 3
		for i in range(times):
			tcr.timeit.start(f"stuff{i + 1}")
			print(f"doing some stuff... (#{i + 1})")
			time.sleep(0.2)
			tcr.timeit.stop(f"stuff{i + 1}", printhook=console)

	def test_breakpoint():
		tcr.breakpoint()
		tcr.breakpoint("asdf")
		tcr.breakpoint("uwu", "owo", "^w^")
		tcr.breakpoint(clear=False)
		tcr.breakpoint(printhook=print)

	def test_getch():
		c(tcr.KeyCodeCompound.vars())

		while 1:
			print("getchs() >>> ", end="", flush=True)
			ch = tcr.getchs()

			print(end="\r")
			c("getchs() ->", ch, ch.__len__())

			if ch == tcr.getchs.CTRL_C:
				break

	def test_asert():
		from tcrutils.misspellings import asert

		asert(lambda: 1 == 1)
		asert(lambda: 1 != 2)

	def test_ifys():
		@tcr.convert.boolify
		def a():
			return 1

		console.debug(f"{a()!r}")

		@tcr.convert.stringify
		def a():
			return 1

		console.debug(f"{a()!r}")

		@tcr.convert.intify
		def a():
			return "10"

		console.debug(f"{a()!r}")

		@tcr.convert.listify
		def a():
			return "asdf"

		console.debug(f"{a()!r}")

		def testify(arg):
			return f"UwU {arg} UwU"

		@tcr.convert.anyify(testify)
		def a():
			return ":3"

		console.debug(f"{a()!r}")

	@(
		lambda f: lambda *a, **kw: (
			lst := f(*a, **kw),
			(None if len(lst) <= 1 else print(f"\n{'\x1b[38;5;3m\x1b[1m'}Average[1:]: {'\x1b[38;5;15m\x1b[1m'}{sum(time_lst := ([x[0] for x in lst])) / len(time_lst):.3f}{'\x1b[0m'}")),
		)
	)
	@repeat(50, no_stdout_after_first=True)
	@(TimeitPartial().decorator(printhook=lambda *a, __sys_stdout=sys.stdout, **kw: (print(*a, **{"end": "\r", "file": __sys_stdout, **kw}), print())))
	def test_print_iterable(π=print_iterable, *, __timeit: TimeitPartial = None, **kwargs):
		import datetime as dt
		from dataclasses import dataclass, field
		from enum import Enum, Flag, IntEnum, IntFlag, ReprEnum, StrEnum, auto
		from functools import partial

		import tcrutils

		orig_π = π
		del π
		π = partial(lambda *a, **kw: [__timeit.start(), orig_π(*a, **kw), __timeit.stop()], **kwargs)

		π("aasd")
		π({"a": 1, "b": "2"})
		π({"a": range(3)})
		π(range(1 << 1000), item_limit=3)
		π(())
		π([])
		π({1, 2})
		π("asdf")
		π(
			[3, 4, 5, range(105)],
			item_limit=4,
			**{x: y for x, y in kwargs.items() if x != "item_limit"},
		)

		def a():
			while True:
				yield 1

		π(a(), item_limit=3, **{x: y for x, y in kwargs.items() if x != "item_limit"})
		π(b"100")
		π(bytearray([10, 20, 30]))
		π(b"uwu\"'")
		π(bytearray([10, 20, 30]), b"abcd", "abcd", r"\1")
		π((None, True, False))
		π({None: None, True: True, False: False})
		π(1)
		π(1.5)
		π(True)
		π(False)
		π(None)
		π(set())
		π({10, 20, 30})
		π(frozenset({"asdf", 1, 3.2j + 1}))
		π({10: 20, 30: 40}.keys())
		π({10: 20, 30: 40}.values())
		π({10: 20, 30: 40}.items())
		π("s p a c e (not uk)")
		π((1,))
		π([[[[]]]])
		π([[[10, 20, [345234582346748673485678673, 40, "a", ()]]]])

		class UnknownThing: ...

		unknown_thing = UnknownThing()
		π(unknown_thing)
		π(UnknownThing)

		### Copied from _collections_abc.py ###
		bytes_iterator = iter(b"asdf")
		π(bytes_iterator)
		bytearray_iterator = iter(bytearray([0xFF, 0x10]))
		π(bytearray_iterator)
		# callable_iterator = ???
		dict_keyiterator = iter({"a": 1, "b": 10, "c": 100}.keys())
		dict_valueiterator = iter({"a": 1, "b": 10, "c": 100}.values())
		dict_itemiterator = iter({"a": 1, "b": 10, "c": 100}.items())
		π(dict_keyiterator)
		π(dict_valueiterator)
		π(dict_itemiterator)
		list_iterator = iter([10, 20, 30])
		π(list_iterator)
		list_reverseiterator = iter(reversed([1, 2, 3]))
		π(list_reverseiterator)
		range_iterator = iter(range(3))
		longrange_iterator = iter(range(1 << 1000))
		π(range_iterator)
		π(longrange_iterator, item_limit=3)
		set_iterator = iter({15, 25, 35})
		π(set_iterator)
		str_iterator = iter("str iterator")
		π(str_iterator)
		tuple_iterator = iter(((30, 40),))
		π(tuple_iterator)
		zip_iterator = iter(zip("abcdefg", range(3), range(4), strict=False))
		π(zip_iterator)

		## misc ##
		π((lambda: (yield))())
		π(range(0))

		## coroutine ##
		async def _coro():
			pass

		_coro = _coro()
		coroutine = _coro
		π(coroutine)
		_coro.close()  # Prevent ResourceWarning
		del _coro

		## asynchronous generator ##
		async def _ag():
			yield

		_ag = _ag()
		async_generator = _ag
		π(async_generator)
		del _ag
		π(range(10))
		π([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"], ["j", "k", "l"]])

		class PrintableObj:
			def __tcr_display__(self=None, **_) -> str:
				return "tcr.fmt-able object" + ("'s instance" if self is not None else "")

		π([PrintableObj])
		π([PrintableObj()])

		import hikari

		π((
			hikari.Status.ONLINE,
			hikari.Status.IDLE,
			hikari.Status.DO_NOT_DISTURB,
			hikari.Status.OFFLINE,
		))

		class PrintableObj2:
			value: int = -1

			def __init__(self, value: int) -> None:
				self.value = value

			def __tcr_display__(self=None, **kwargs) -> str:
				from tcrutils.dict import clean_dunder_dict

				return fmt_iterable(
					clean_dunder_dict((self if self is not None else PrintableObj2).__dict__),
					_force_next_type=PrintableObj2,
					_i_am_class=not self,
					**kwargs,
				)

		π(PrintableObj2)
		π(PrintableObj2(69))

		class Client:
			test: str

			def __init__(self, test: str) -> None:
				self.test = test

			def __repr__(self) -> str:
				return f"{self.__class__.__name__}(test={self.test!r})"

		π(Client("test"))
		π(0x7FFFFFFF)
		π(tcr_types.HexInt(0x7FFFFFFF))
		π(float | int)
		π(str)
		π([[[[[[[[[[[[]]]]]]]]]]]], let_no_indent=False)
		π([tcr_types.QuotelessString("quoteless string")] * 3)
		π({
			"a": [
				"nya",
				"owo",
				"uwu",
				{
					"12": 34,
					"56": 78,
				},
				[10, 20, 30],
			]
		})
		π({
			"b": [],
		})
		π({
			"b": 2,
		})
		π({
			"b": 2,
			"d": 4,
		})
		π({
			"b": None,
		})

		print()  # Now
		datetime = dt.datetime.now()
		π(datetime)
		π(datetime.date())
		π(datetime.time())

		print()  # In the future by 1 minute
		datetime2 = dt.datetime.now() + dt.timedelta(minutes=1)
		π(datetime2)
		π(datetime2.date())
		π(datetime2.time())

		print()  # In the past by 1 minute
		datetime2 = dt.datetime.now() + dt.timedelta(minutes=-1)
		π(datetime2)
		π(datetime2.date())
		π(datetime2.time())

		print()
		π(dt.timedelta(days=1, hours=1, minutes=1, seconds=1))
		# NOTE: TIMEDELTA PRETTY PRINTING WAS NEVER IMPLEMENTED, DOTN BE SURPRISED THERES NO IMPL FOR IT AND IT LOOKS LIKE AN UNKNOWN OBJECT WHEN PRINTED!!!

		print()
		ts = tcr_types.UnixTimestampInt(1719949074443)

		π(ts, _raise_errors=True)
		π(ts.to_datetime(), _raise_errors=True)

		print()
		π(tcr_types.HexInt(2, leading_zeroes=2))
		π(tcr_types.HexInt(3, leading_zeroes=3))
		π(tcr_types.HexInt(4, leading_zeroes=4))
		π(tcr_types.HexInt(5, leading_zeroes=5))
		π(tcr_types.HexInt(6))
		print()
		π(tcrutils)
		π([tcrutils])
		π((tcrutils,))
		print()
		π("nya")
		π('n"ya')
		π("n'ya")
		print()

		class EAnimal(Enum):
			FOX = "Fox"
			WOLF = "Wolf"

		class EAnimalInt(IntEnum):
			FOX = 1
			WOLF = 2

		class EAnimalComplex(complex, ReprEnum):
			FOX = 1 + 0j
			WOLF = 1 + 1j

		class EAnimalStr(StrEnum):
			FOX = "Fox"
			WOLF = "Wolf"
			A = "A"
			B = "B"
			C = "C"

		π(EAnimal)
		π(EAnimalInt)
		π(EAnimalComplex)
		π(EAnimalStr)
		print()
		π(EAnimal.FOX)
		π(EAnimalInt.FOX)
		π(EAnimalComplex.FOX)
		π(EAnimalStr.FOX)
		print()

		class IntCTF(IntFlag):
			A = 1 << 0
			B = 1 << 1
			C = 1 << 2
			D = 1 << 2

		class CTF(Flag):
			CA = 1 << 0
			CB = 1 << 1
			CC = 1 << 2
			CD = 1 << 3

		π(IntCTF)
		π(CTF)
		print()
		π(IntCTF.A)
		π(CTF.CA)
		π(CTF.CA | CTF.CB)
		ab = IntCTF.A | IntCTF.B
		π(ab)
		π(ab | IntCTF.C)
		print()

		class AutoEnum(Enum):
			A = auto()
			B = auto()
			C = auto()
			D = auto()

		π(AutoEnum)
		print()
		π(AutoEnum.A)

		class TestTCRFmt:
			value: str

			def __init__(self, value: str = "uwu") -> None:
				self.value = value

			def __tcr_fmt__(self=None, *, fmt_iterable, **kwargs) -> str | None:
				if self is None:
					return None

				return fmt_iterable(self.value, **kwargs)

		print()

		instance1 = TestTCRFmt(value="nya")
		instance2 = TestTCRFmt()

		π(instance1)
		π(instance2)
		π(TestTCRFmt)
		print()

		@dataclass
		class TestDataclass:
			value: str
			value2: str = field(default="uwu")

		π(hikari)
		π(sys)
		π(tcrutils)
		π(TestDataclass)
		π(TestDataclass(value="nya"))
		print()
		π(p.Path().absolute())
		π(p.Path("uwu"))
		π(p.PurePath("uwu"))
		π(p.PurePath("/uwu"))
		print()
		π(hikari.Status)
		π(hikari.ActivityType)
		π(hikari.ActivityType.CUSTOM)
		print()
		bf_code = tcrutils.types.BrainfuckCode(",asdf>.<++[uwu-]nya")
		π(bf_code)
		print()
		π(...)
		print()
		π(sys.version_info)

		print()
		π(
			joke.echo,
			joke.echo[:],
			joke.echo[::-1],
		)
		print()

		class Reprer:
			def __init__(self, *args, **kwargs) -> None:
				self.args = args
				self.kwargs = kwargs

			def __repr__(self) -> str:
				if not self.args and not self.kwargs:
					return f"{self.__class__.__name__}()"
				elif self.args and self.kwargs:
					args_str = ", ".join(map(repr, self.args))
					kwargs_str = ", ".join(f"{k}={v!r}" for k, v in self.kwargs.items())

					return f"{self.__class__.__name__}({args_str}, {kwargs_str})"
				elif self.args:
					args_str = ", ".join(map(repr, self.args))

					return f"{self.__class__.__name__}({args_str})"
				elif self.kwargs:
					kwargs_str = ", ".join(f"{k}={v!r}" for k, v in self.kwargs.items())

					return f"{self.__class__.__name__}({kwargs_str})"
				else:
					raise ValueError("What?")

		π(Reprer)
		π(Reprer())
		π(Reprer("nya"))
		π(Reprer("nya", "uwu"))
		π(Reprer("nya", "uwu", "owo", "hihi", "mrrraaaw :3"))
		π(Reprer("nya", "uwu", "owo", "hihi", "mrrraaaw :3", x="nyaaaa", y="uwu"))
		π(Reprer(x="nya", y="uwu"))
		π(Reprer(x="nya"))

		π({1: 2})
		π({1: 2, 3: 4})
		π([1, 2, 3, 4])
		π([1, 2, 3, 4, 5])

		from tcrutils.result import Result

		class ListResult(Result[list, ValueError]): ...

		res1 = ListResult.new_ok(["nya", 123, 3 + 2j, True, None])
		res2 = ListResult.new_err(ValueError("wal-konia-ue ełrołr"))

		π(
			ListResult,
			res1,
			res2,
		)
		π(
			[
				"\x011",
				"\x01a",
				"\x001",
				"\x00a",
			],
			[
				'"\U00042346',
				'"\U00012345',
				"'\"nya",
			],
		)
		print()

		class Rainbow:
			__tcr_rainbow__ = True

		class Rainbow2:
			__tcr_rainbow__ = "reynbou"

		π(
			Rainbow,
			Rainbow2,
			Rainbow(),
			Rainbow2(),
			tcrutils,
		)
		print()
		π(type.__mro__)
		print()

		class A(pydantic.BaseModel):
			a: int
			b: int
			c: int

		class B(pydantic.BaseModel): ...

		π(A(a=1, b=2, c=3))
		π(A)
		π(pydantic.BaseModel)
		π(B)
		π(B())

		print()
		from tcrutils.class_ import new_cell

		π(new_cell)
		π(new_cell())
		cell = new_cell()
		cell.cell_contents = str
		π(cell)
		print()
		π(dt.datetime.now())
		π(dt.datetime.now(tz=dt.UTC))
		π(dt.datetime.now().replace(microsecond=0))
		π(dt.datetime.now(tz=dt.UTC).replace(microsecond=0))
		π(dt.datetime(1, 1, 1, 0, 0, 0, 0))
		π(dt.datetime(1, 1, 1, 0, 0, 0, 0, tzinfo=dt.UTC))
		π(dt.time(0, 0, 0, 0))
		π(dt.time(0, 0, 0, 0, tzinfo=dt.UTC))
		π(dt.date(1, 1, 1))
		print()

		class PydanticModel(pydantic.BaseModel):
			a: int
			b: int
			c: int

		π(PydanticModel(a=1, b=2, c=3), prefer_pydantic_better_dump=True)
		π(PydanticModel, prefer_pydantic_better_dump=True)
		print()

	def test_markdown():
		from tcrutils import codeblock, uncodeblock

		console.debug(codeblock("asdf"))
		console.debug(codeblock("uwu", langcode="owo"))
		console.debug(codeblock(""))
		console.debug([a := codeblock("asxxxxxxxxxdf", langcode="py", max_length=17), len(a)])
		console.debug(uncodeblock(codeblock("hihi", langcode="py")))
		console.debug(uncodeblock("```py\n:3```"))

	def test_extract_error():
		from tcrutils import extract_error

		console(extract_error(ValueError("asdf")))
		console(extract_error(ValueError("uwu")))
		console(extract_error(ValueError()))
		console(extract_error(ValueError))
		console(extract_error(ValueError("Ewwow~!"), raw=True), print_iterable_=False)

	def test_sort():
		@tcr.timeit
		def bogo_sort():
			console(tcr.bogo_sort(tcr.shuffled(list(range(5)) * 2)))

		@tcr.timeit
		def stalin_sort():
			console(tcr.stalin_sort(tcr.shuffled(list(range(100)) * 2)))

		bogo_sort()
		stalin_sort()

	def test_print_block():
		from tcrutils import print_block

		print_block("Test")
		print_block("OwO", "#", margin=1, border=10, padding=2)
		console(print_block("UwU", raw=True, padding_top=2), print_iterable_=False)

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

		console(timestr.to_datestr(a))

	def test_console_or_ror():
		print(console | "UwU")
		print("UwU" | console)

	def test_christmas_tree():
		# print(tcr.christmas_tree())
		print(tcr.christmas_tree(symbol="C#"))
		# print(tcr.christmas_tree(symbol="C+", height=3))

	def test_recursive_sum():
		console(tcr.recursive_sum([1, 2, 3, 4, [99, 4, 5]]))

	def test_terminal():
		print(tcr.terminal.size, type(tcr.terminal.size), complex(tcr.terminal.size))

	def test_get_token():
		rass(tcr.get_token)(FileNotFoundError)

	def test_thisdir():
		console(os.getcwd())
		console(tcr.path.thisdir(chdir=True))
		console(os.getcwd())

	def test_able():
		ass(tcr.able(int, "ff8000", base=16), (True, 16744448), expr="tuple(a) == b")
		ass(tcr.able(int, "ff8000"), expr="not a")

	def test_insist():
		from functools import partial

		from tcrutils import insist

		number = int(insist(partial(input, "Input a number: "), partial(tcr.able, int)))

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
		from tcrutils.sdb import ShelveDB

		DB_DIRECTORY = (p.Path(__file__).parent / "test_db").absolute()
		DB_DIRECTORY.mkdir(exist_ok=True)

		class Database(ShelveDB):
			directory = DB_DIRECTORY

			defaults = {
				"r": list,
			}

		c(Database.exists("db1"))
		c(Database.exists("db0"))

		db1 = Database("db1")

		c(db1)

		db1.clear()

		c(db1)

		c(db1["r"])

		c(db1)

		c(db1.get_directory())
		c(db1.get_path())

		db = Database("db")

		db["OwO"] = "UwU"
		console(db)

		del db["OwO"]
		console(db)

		db.setdefault("a", "A")
		console(db)
		db.setdefault("b", "B")
		db.setdefault("c", "C")
		db.setdefault("d", "D")
		console(db)

		console('db.pop("a")=', db.pop("a"))
		console("db=", db)
		console("db.popitem()=", db.popitem())
		console("db=", db)
		console("db.popitem()=", db.popitem())
		console("db=", db)
		console("db.popitem()=", db.popitem())
		console("db=", db)

	def test_fmt_iterable(*, printhook=print, syntax_highlighting=True, **kwargs):
		kwargs["syntax_highlighting"] = syntax_highlighting
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

		console(hasmanyattrs(cld, *"attr1.clear".split(".")))
		console(getmanyattrs(cld, *"attr1.clear".split(".")))

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
		console(
			tcr.clean_dunder_dict(
				{
					"UwU": "OwO",
					"__UwU__": "__OwO__",
					"__UwU": "__OwO",
					"_UwU": "_OwO",
				},
				strategy=2,
			)
		)

	def test_class():
		class SingleTuple(tcr.Singleton, tuple): ...

		tup = SingleTuple(("tup1",))
		tup2 = SingleTuple(("tup2",))

		console(tup)  # -> ('tup1',)
		console(tup2)  # -> ('tup1',)

	def test_overload():
		class A(tcr.Overload):
			@tcr.overload
			def f(self, arg1: int):
				console("1-arg f:", arg1)

			@tcr.overload
			def f(self, arg1: int, arg2: int):  # noqa: F811
				console("2-arg f:", arg1, arg2)

			@tcr.overload
			def f(self, arg1: str):  # noqa: F811
				console("str-arg f:", arg1)

		a = A()

		a.f(10)
		a.f(20, 30)
		a.f("")

	def test_raises():
		from tcrutils import raises

		ass(raises((lambda x: 1 / x), x=1)(ZeroDivisionError), False)
		ass(raises((lambda x: 1 / x), x=0)(ZeroDivisionError), True)

	def test_ass():
		ass("Expected pass", "Expected pass")
		ass(2137, 69, suppress=True)
		ass(1, 2, expr="a < b")
		ass("1", expr=int)
		ass([1], expr=bool)
		ass([], expr=bool, suppress=True)
		ass([], expr=list, suppress=True)

	def test_discord_ifys():
		rass(tcr.discord.IFYs.userify, -1)(ValueError)
		ass(tcr.discord.IFYs.userify(1 << 63), f"<@{1 << 63}>")
		rass(tcr.discord.IFYs.userify, 1 << 63 + 1)(ValueError)
		ass(tcr.discord.IFYs.userify(1234), "<@1234>")
		ass(tcr.discord.IFYs.userbangify(1234), "<@!1234>")
		ass(tcr.discord.IFYs.channelify(1234), "<#1234>")
		ass(tcr.discord.IFYs.commandify("cmd", 1234), "</cmd:1234>")
		ass(tcr.discord.IFYs.emojify("emo", 1234), "<:emo:1234>")
		ass(tcr.discord.IFYs.emojify("uwu", 69, animated=True), "<a:uwu:69>")
		ass(tcr.discord.IFYs.timeify(1), "<t:1>")
		ass(tcr.discord.IFYs.timeify(1, "F"), "<t:1:F>")
		rass(tcr.discord.IFYs.timeify, 1, "r")(ValueError)
		ass(tcr.discord.IFYs.timeify(1, "F"), "<t:1:F>")

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

		async def a(): ...

		a()

	def test_error_catcher():
		tcr.ErrorCatcher()
		# import rich.traceback
		# rich.traceback.install()

		raise ValueError("err")

	def test_console_new():
		console("test")
		console.log("test")
		console.error("test")
		console.warn("test")
		console.critical("test")

	def test_dunder_version():
		console({
			"__version__": tcr.__version__,
			"__name__": tcr.__name__,
			"__file__": tcr.__file__,
		})

	def test_dotdicts():
		from tcrutils import Undefined

		dd = tcr.DotDict({"a": 1, "b": 2})
		ass(dd.a, 1)
		ass(dd.b, 2)
		rass(lambda: dd.c)(KeyError)
		del dd.a
		ass(dd, {"b": 2})

		dd = tcr.DotDict({"a": 1, "b": {"c": 3}})
		ass(dd.b.c, 3)

		jsd = tcr.JSDict({"a": 1, "b": 2})
		ass(jsd["a"], 1)
		ass(jsd["b"], 2)
		ass(jsd["c"], Undefined)

		jsdd = tcr.JSDotDict({"a": 1, "b": 2})
		ass(jsdd.a, 1)
		ass(jsdd.b, 2)
		ass(jsdd.c | 3, 3)
		del jsdd.asdfa  # Nothing should happen because jsdict will suppress the invalid item - because javascript

	def test_null():
		from tcrutils import Null, Undefined

		console(Null)
		console(Undefined)
		ass(Null is Null.__class__())
		ass(Undefined is Undefined.__class__())
		ass(Undefined is not Null)
		console(type(Null))
		console(type(Undefined))
		console(str(Null))
		console(repr(Null))
		console(str(Undefined))
		console(repr(Undefined))
		ass(Null | 0, 0)
		ass(Null | 1, 1)
		ass(0 | Null, 0)
		ass(1 | Null, 1)
		ass(Undefined | 0, 0)
		ass(Undefined | 1, 1)
		ass(0 | Undefined, 0)
		ass(1 | Undefined, 1)
		console(Null | Undefined)
		console(Undefined | Null)
		console(Undefined | Undefined)
		console(Null | Null)

	def test_get_caller_line_number():
		console(tcr.get_lineno())
		console(tcr.get_file_colon_lineno())
		console(tcr.get_file_colon_lineno(additional_offset=10))

	def test_diff():
		console(
			{
				1: 2,
				3: 2,
				5: 6,
			},
			diff=True,
		)
		console(
			{
				1: 2,
				3: 4,
				5: 6,
			},
			diff=True,
		)
		console(
			{
				1: 4,
				3: 4,
				6: 4,
				7: 4,
				5: 6,
			},
			diff=True,
		)

	async def test_execute():
		execute = tcr.Execute(
			placeholders={
				"uwu": lambda *_, **__: "UwU",
				"nyaaa": lambda *_, **__: "NYAAA{}AAA ;3",
				"mirror": lambda ___, param1, *_, **__: param1[::-1],
				"mirrorUwU": lambda ___, param1, *_, **__: param1[::-1] + "hihi",
			}
		)

		console(await execute("asdfasdfgsdfg {uwu} {nyaaa} {mirror{uwu}|2345}"))

	def test_divstring():
		s = tcr.SlashableString("uwu")

		a = s / s / s

		console.debug(a)

	def test_cint():
		i: int = tcr.CInt(11)

		c(i)
		++i  # noqa
		c(i)

		print()

		c(i)
		-i  # noqa
		c(i)
		-i  # noqa
		c(i)

		print()

		c(--i.bit_length())  # noqa

	def test_generate_type_hinter2():
		imgui = __import__("imgui")

		tcr.generate_type_hinter(imgui, print=True, clipboard=False)

	async def test_dynamic_responses():
		EXECUTE = tcr.dynamic_responses.DynamicResponseBuilder(
			tcr.dr.placeholder_set.ALL_NON_DISCORD,
			parens=("{", "}"),
			error_on_missing_placeholder=False,
		)

		ass.error_func = lambda *_, **__: ...

		ass(
			await EXECUTE("owo {add|1|{add|2|2}} asdfasdfgsdfg {uwu} {nyaaa}"),
			expr="bool(a) == b",
		)
		# This shall forever stay executed to signify a potential fuckup in the nested placeholder capabilities

		if __TEXT := True:
			print()
			c("COMMENT", quoteless=True)
			ass(await EXECUTE("cu{comment|comment}ment"), "cument")
			ass(await EXECUTE("#cu{#|comment}ment"), "#cument")
			ass(await EXECUTE("//cu{//|comment}ment"), "//cument")
			print()
			c("VAR", quoteless=True)
			ass(await EXECUTE("{var|var1|nya}{var1} {var|var1}"), "nya nya")
			print()
			c("TEST", quoteless=True)
			ass(await EXECUTE("{test|a|a|T|F}F2"), "TF2")
			ass(await EXECUTE("T{test|a|ż|F|F}2"), "TF2")
			ass(await EXECUTE("{test|a|a}"), "true")
			ass(await EXECUTE("{test|a|ż}"), "false")
			ass(await EXECUTE("{test|a}"), "{test|a}")
			ass.total(prefix="\n")

		if __MATH := True:
			c.hr()
			print()
			c("ADD", quoteless=True)
			ass(await EXECUTE("{add}"), "0")
			ass(await EXECUTE("{add|4}"), "4")
			ass(await EXECUTE("{add|1|1}"), "2")
			ass(await EXECUTE("{add|1|1|2.4}"), "4.4")
			print()
			c("SUBTRACT", quoteless=True)
			ass(await EXECUTE("{sub}"), "0")
			ass(await EXECUTE("{sub|5}"), "5")
			ass(await EXECUTE("{sub|1|2}"), "-1")
			ass(await EXECUTE("{sub|1|2|3}"), "-4")
			print()
			c("MULTIPLY", quoteless=True)
			ass(await EXECUTE("{mul}"), "1")
			ass(await EXECUTE("{mul|3|3}"), "9")
			ass(await EXECUTE("{mul|3|3|4}"), "36")
			ass(await EXECUTE("{mul|2|3.4}"), "6.8")
			print()
			c("DIVIDE", quoteless=True)
			ass(await EXECUTE("{div}"), "1")
			ass(await EXECUTE("{div|3}"), "3")
			ass(await EXECUTE("{div|1|2}"), "0.5")
			ass(await EXECUTE("{div|15|3|5}"), "1")
			print()
			c("FLOOR DIVIDE", quoteless=True)
			ass(await EXECUTE("{floordiv}"), "1")
			ass(await EXECUTE("{fdiv|3}"), "3")
			ass(await EXECUTE("{fdiv|1|2}"), "0")
			ass(await EXECUTE("{fdiv|34|3}"), "11")
			print()
			c("POWER", quoteless=True)
			ass(await EXECUTE("{pow}"), "{pow}")
			ass(await EXECUTE("{pow|3}"), "9")
			ass(await EXECUTE("{pow|2|3}"), "8")
			ass(await EXECUTE("{pow|2|2|2|2}"), "256")
			print()
			c("MOD", quoteless=True)
			ass(await EXECUTE("{mod}"), "{mod}")
			ass(await EXECUTE("{mod|5}"), "5")
			ass(await EXECUTE("{mod|15|3}"), "0")
			ass(await EXECUTE("{mod|15|2|3}"), "1")
			print()
			c("ROUND", quoteless=True)
			ass(await EXECUTE("{round}"), "{round}")
			ass(await EXECUTE("{round|1.3}"), "1")
			ass(await EXECUTE("{round|1.7}"), "2")
			ass(await EXECUTE("{round|1.5}"), "2")
			print()
			c("FLOOR", quoteless=True)
			ass(await EXECUTE("{floor}"), "{floor}")
			ass(await EXECUTE("{floor|6.1}"), "6")
			ass(await EXECUTE("{floor|6.9}"), "6")
			print()
			c("CEIL", quoteless=True)
			ass(await EXECUTE("{ceil}"), "{ceil}")
			ass(await EXECUTE("{ceil|9.1}"), "10")
			ass(await EXECUTE("{ceil|9.9}"), "10")
			ass.total(prefix="\n")

		if __DEBUG := True:
			c.hr()
			c("DEBUG", quoteless=True)
			ass.total(prefix="\n", ignore_empty=False)

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
"""[1:-1]  # noqa: F841, RUF100

		T_SERVER = """
## Server
Name: {server|name}
ID: {server|id}
"""[1:-1]  # noqa: F841, RUF100

		CURRENT_TEST = T_SERVER

		@ACL.include
		@arc.slash_command(*2 * ["test_dynamic_responses"])
		async def cmd_test_dynamic_responses(
			ctx: arc.Context,
			text: arc.Option[str, arc.StrParams("The reminder syntax (use /help for help)")] = None,
		) -> None:
			if text is None:
				text = CURRENT_TEST

			result = await EXECUTE(
				text,
				**{
					"ctx": ctx,
				},
			)

			c(result.resp)

			await ctx.respond(**result.resp)

		@BOT.listen(hikari.MessageCreateEvent)
		async def on_message(event: hikari.MessageCreateEvent) -> None:
			if event.author_id == BOT.get_me().id:
				return

			if hasattr(event, "guild_id") and event.channel_id != 1125889206586183682:
				return

			if not event.content:
				return

			result = await EXECUTE(
				event.content if event.content != "t" else CURRENT_TEST,
				**{
					"event": event,
				},
			)

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
			tcr.ensure_depencencies.Dependency(import_as="requests"),
			tcr.ensure_depencencies.Dependency(import_as="hikari"),
			tcr.ensure_depencencies.Dependency(import_as="lightbulb", pip_install_as="hikari-lightbulb"),
			tcr.ensure_depencencies.Dependency(import_as="abd", pip_install_as="abd"),
		)

		ensure_dependencies()

	def test_dpy():
		while a := input("Escape markdown >>> "):
			c(tcr.discord.escape_markdown(a))

		while a := input("Remove markdown >>> "):
			c(tcr.discord.remove_markdown(a))

		while a := input("Escape mentions >>> "):
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
				await ctx.respond("Yes clicked")

			async def no(btn: miru.Button, ctx: miru.ViewContext):
				await ctx.respond("No clicked")

			class CustomButton(miru.Button):
				async def callback(self, ctx: miru.ViewContext):
					await ctx.respond("Custom clicked")

			class CustomSelect(miru.TextSelect):
				async def callback(self, ctx: miru.ViewContext):
					await ctx.respond("Custom selected: " + repr(self.values[0]))

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
				return f"Button(label={self.label!r})"

		class YesButton(Button, label="Yes"): ...

		class NoButton(Button, label="No"): ...

		y = YesButton()
		c(repr(y))  # -> Button(label='Yes')
		n = NoButton()
		c(repr(n))  # -> Button(label='No')
		n2 = NoButton(label="Nuh uh")  # Overridden
		c(repr(n2))  # -> Button(label='Nuh uh')

	def test_with_overrides():
		from dataclasses import dataclass

		@dataclass(kw_only=True)
		class A:
			a: int
			b: str

			@tcr.with_overrides("a", "b")
			def get_a(self, *, a: int, b: str):
				return a, b

		a = A(a=1, b="b")

		c(a.get_a())
		c(a.get_a(a=2))
		c(a.get_a(b="c"))
		c(a.get_a(a=2, b="c"))

	def test_tstr():
		import datetime as dt

		import pytz

		STRFTIME_FORMAT_SPECIFIER = "%a, %Y-%m-%d %H:%M:%S"

		tcr.timeit.start("timezone")

		tzinfo = pytz.timezone("Europe/Warsaw")

		tcr.timeit.stop("timezone")

		tstr = tcr.TStr(tzinfo=tzinfo, fix_timezone=True)

		now1 = tstr.to_datetime("0").replace(microsecond=0)
		now2 = dt.datetime.now(tz=tzinfo).replace(microsecond=0)

		console(now1.strftime(STRFTIME_FORMAT_SPECIFIER))
		console(now2.strftime(STRFTIME_FORMAT_SPECIFIER))
		ass(now1, now2)
		ass(now1 - now2, dt.timedelta(0))
		ass(now1.tzinfo, now2.tzinfo)

		print()
		ass.total()
		print()

		ass(tstr.to_int("0"), 0)
		ass(tstr.to_int("1s"), 1)
		ass(tstr.to_int("-1h"), -3600)
		print()
		console(tstr.to_datetime("wed").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("mon").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("::").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("::!1.1.0").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("::1").strftime(STRFTIME_FORMAT_SPECIFIER))  # localhost
		print()
		console(tstr.to_datetime("10:").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("23:59:59").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("1.").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("28.").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("1d!wed").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("wed!1d").strftime(STRFTIME_FORMAT_SPECIFIER))
		print()
		console(tstr.to_datetime("1rev").strftime(STRFTIME_FORMAT_SPECIFIER))
		print()
		console(tstr.to_datetime(":").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("0:").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(tstr.to_datetime("23:59:59").strftime(STRFTIME_FORMAT_SPECIFIER))
		console("1.", tstr.to_datetime("1.").strftime(STRFTIME_FORMAT_SPECIFIER))
		console("28.", tstr.to_datetime("28.").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(
			f"{now1.day}.",
			tstr.to_datetime(f"{now1.day}.").strftime(STRFTIME_FORMAT_SPECIFIER),
		)
		console("1.!::", tstr.to_datetime("1.!::").strftime(STRFTIME_FORMAT_SPECIFIER))
		console("28.!::", tstr.to_datetime("28.!::").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(
			f"{now1.day}.!::",
			tstr.to_datetime(f"{now1.day}.!::").strftime(STRFTIME_FORMAT_SPECIFIER),
		)
		console("1.!14::", tstr.to_datetime("1.!14::").strftime(STRFTIME_FORMAT_SPECIFIER))
		console("28.!14::", tstr.to_datetime("28.!14::").strftime(STRFTIME_FORMAT_SPECIFIER))
		console(
			f"{now1.day}.!14::",
			tstr.to_datetime(f"{now1.day}.!14::").strftime(STRFTIME_FORMAT_SPECIFIER),
		)
		console(f"wed!:", tstr.to_datetime(f"wed!:").strftime(STRFTIME_FORMAT_SPECIFIER))
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
		rass(tstr.to_int, "1")(ValueError)
		rass(tstr.to_int, "nya")(ValueError)
		print()
		ass.total()

	def test_default():
		class A(tcr.DefaultsGetSetAttr):
			defaults = {
				"nya": int,
			}

		a = A()

		a.uwu = "owo"
		c(a.nya)
		c(a.uwu)
		c(tcr.dir3(a))

		print()

		class B(tcr.DefaultsGetAttr):
			defaults = {
				"nya": int,
			}

		b = B()

		b.uwu = "owo"
		c(b.nya)
		c(b.uwu)
		c(tcr.dir3(b))

		print()

		class C(tcr.DefaultsGetSetItem):
			defaults = {
				"nya": int,
			}

		ce = C()

		ce["owo"] = 1

		c(ce["nya"])
		c(ce["owo"])
		c(ce.keys())

		print()

		class D(tcr.DefaultsGetItem):
			defaults = {
				"nya": int,
			}

		d = D()

		d["owo"] = 1

		c(d["nya"])
		c(d["owo"])
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

		class TestCIM_DB(
			tcr.ShelveDB,
			metaclass=tcr.CachedInstancesMeta,
			max_instances=2,
			max_time=2,
			restore_method="restore",
		):
			directory = str((p.Path(__file__).parent / "test_db").absolute())

		db = TestCIM_DB("tedddst145345")

		c(db.iter_all_path_names())

		c(db)
		db.close()
		db["asdf"] = 1
		c(db["asdf"])
		c(db)
		db.restore()
		c(db)

	def test_dir_recursive():
		class A(dict):
			def test(self):
				return "nya"

			a = 1

		a = A()

		a.b = "b"

		c(tcr.vars2(a, vars=tcr.vars_recursive))

	def test_err_denoted():
		class A(list, tcr.ErrDenoted): ...

		class BError(Exception, tcr.ErrDenoted): ...

		a = A()

		b = BError()

		c(a, a.is_err())
		c(b, b.is_err())

	def test_is_snowflake():
		ass(tcr.discord.is_snowflake(0b1111111111111111111111111111111111111111111111111111111111111111))
		ass(tcr.discord.is_snowflake(0b1111111111111111111111111111111111111111111111111111111111111110))
		ass(
			tcr.discord.is_snowflake(0b1111111111111111111111111111111111111111111111111111111111111111 + 1),
			False,
		)
		ass(tcr.discord.is_snowflake(0))
		ass(tcr.discord.is_snowflake(-1), False)

	def test_console_fmt():
		obj = [69, True, None, tcr.Null]
		s = "Hewwo"

		c(obj)
		c(s)
		c(obj, s, s)

		c.hr()

		c.log(obj)
		c.log(s)
		c.log(obj, s, s)

		c.hr()

		c.warn(obj)
		c.warn(s)
		c.warn(obj, s, s)

		c.hr()

		c.error(obj)
		c.error(s)
		c.error(obj, s, s)

		c.hr()

		c.critical(obj)
		c.critical(s)
		c.critical(obj, s, s, s)

	def test_console_callsite(c=c):
		c.include_callsite = True
		c(1)
		c.log(1)
		c.warn(1)
		c.error(1)
		c.critical(1)
		c("nya")
		c.log("nya")
		c.warn("nya")
		c.error("nya")
		c.critical("nya")
		c.include_callsite = None

	def test_fucking_pydantic_model_dump_my_ass():
		from pydantic import BaseModel
		from tcrutils import c

		class I(BaseModel):
			i: int

			def __hash__(self):
				return self.i

		class Container(BaseModel):
			s: set[I]

		co = Container(s={I(i=1), I(i=2), I(i=3)})

		c(co)

	def test_joke_pointer():
		v = [1, 2, 3]

		ptr = tcr.joke.Pointer(v)

		ptr2 = tcr.joke.Pointer(ptr)

		c(v, padding=" v=")
		c(ptr, padding=" ptr=")
		c(ptr2, padding=" ptr2=")
		c(*ptr, padding=" *ptr=")

		(_temp,) = (*ptr,)  # fmt: off

		c(*_temp, padding=" **ptr2=")

	def test_eval_fback():
		c(tcr.eval_fback("locals()"))

	def test_console_with_header():
		hc = c.with_expr_header("zoo", literal=True).with_expr_header('__name__ if __name__ != "__main__" else None')

		hc({1, 2, 3, 4})
		hc.debug({1, 2, 3, 4})
		hc.log("Nyaaa", "uwu")
		hc.error("owo")

	def test_console_with_eval():
		var = "wahr"  # noqa: F841

		c("1+1=", eval=True)
		c("var=", eval=True)
		c("c=", eval=True)
		c("nya=", ("c", "uwu"))

	def test_repl():
		import tcrutils.repl as repl
		from tcrutils.print import FMTC
		from tcrutils.repl import node
		from tcrutils.terminal import terminal

		class TestingRepl(repl.Repl):
			def printhook(self, last_char: str | None, *submitted_nodes: node.Node):
				prompt = self.printhook_prompt(last_char, *submitted_nodes)

				body = "".join(self.display_node(n) for n in submitted_nodes)

				cursor = "_" if submitted_nodes and not isinstance(submitted_nodes[-1], node.IncompleteNode) and submitted_nodes[-1].text and submitted_nodes[-1].text[-1] in " \t" else ""

				print(FMTC._ + terminal.width * " " + "\r" + f"{prompt} {body}{FMTC._}{cursor}", end="\r")

			def display_node(self, n: node.Node, /) -> str:
				match n:
					case node.EllipsisNode(text=text):
						return f"{FMTC.DECIMAL}{text}{FMTC._}"

				return super().display_node(n)

			no_enter_on_unknown_or_incomplete = "-f" not in sys.argv

		repl = TestingRepl(
			node.IrrefutableNode(
				node.KeywordNode(
					"any",
					node.WordBreakNode("../*"),
					node.MatchEverythingNode(),
				),
				node.KeywordNode(
					"p",
					node.WordBreakNode(
						"../*",
					),
					node.PathNode(
						valid_state=node.PathNode.ValidState.EXISTS_FILE,
						filename_regex=r"^.*\.py$",
					),
				),
				node.KeywordNode(
					"t",
					node.WordBreakNode("../*"),
					node.TimestrNode(
						node.WordBreakNode(
							node.PyIdentifierNode(),
						),
						node.IrrefutableNode(),
					).with_tzinfo(),
				),
				n_makeshift_junc := node.UnreachableNode(
					node.WordBreakNode("/makeshift-junc/*"),
					node.KeywordNode(
						"then",
						"/new/*",
					),
					name="makeshift-junc",
				),
				node.KeywordNode(
					"new",
					node.WordBreakNode(
						"../*",
						node.EllipsisNode(*n_makeshift_junc.children, node.IrrefutableNode()),
						node.IntNode(*n_makeshift_junc.children, node.IrrefutableNode()),
						node.FloatNode(*n_makeshift_junc.children, node.IrrefutableNode()),
						node.PyIdentifierNode(*n_makeshift_junc.children, node.IrrefutableNode()),
						# node.DoublequoteStrNode(*makeshift_junc.children, node.IrrefutableNode()),
						# node.SinglequoteStrNode(*makeshift_junc.children, node.IrrefutableNode()),
						node.StringNode(*n_makeshift_junc.children, node.IrrefutableNode()),
						node.ListOfStrOrInt(*n_makeshift_junc.children, node.IrrefutableNode()),
					),
				),
				node.KeywordNode(
					"dupa",
					node.WordBreakNode("../*"),
					node.StringNode(*n_makeshift_junc.children, node.IrrefutableNode()),
				),
				node.KeywordNode(
					"ass",
					node.WordBreakNode("../*"),
					node.ListOfInt(*n_makeshift_junc.children, node.IrrefutableNode()),
				),
				node.AliasKeywordNode(
					alias_name="n",
					target_path="/new",
				),
				node.KeywordNode("q"),
				node.IrrefutableNode(),
			)
		)

		c(repl.nodes)
		c.hr(newlines_on_both_sides=False)
		c("no_enter_on_unknown_or_incomplete=", repl.no_enter_on_unknown_or_incomplete, withprefix=False)

		def cmd_dupa(n: node.StringNode):
			c("Dupa haha -> ", n.parse())
			return True

		def cmd_timestr(this: node.TimestrNode):
			c("sigma")
			c(this._parsed)
			return True

		def cmd(n: node.Node, *ns: node.Node) -> bool:
			match n:
				case node.KeywordNode("q"):
					exit(0)
				case node.KeywordNode("new"):
					c("new ->", ns)
					return True
				case node.KeywordNode("dupa"):
					return cmd_dupa(*ns)
				case node.TimestrNode():
					return cmd_timestr(n, *ns)

		class UnaccountedForNodesError(RuntimeError):
			nodes: tuple[node.Node]

			def __init__(self, *nodes: node.Node, syntax_highlighting: bool = True):
				self.nodes = nodes
				super().__init__(fmt_iterable(nodes, syntax_highlighting=syntax_highlighting))

		while 1:
			submitted_nodes = repl()
			print()

			if not submitted_nodes:
				continue

			if 0:
				if cmd(*submitted_nodes):
					continue

				raise UnaccountedForNodesError(*submitted_nodes)

			match submitted_nodes[0]:
				case node.KeywordNode("q"):
					exit(0)

			c(submitted_nodes)

	def test_typehints():
		class Eent(int): ...

		@tcr.force_keyword_only_typehints(key=lambda v, t: v.__class__ is t)
		def nya(*, a: int, b: int) -> str:
			return f"{a!r}, {b!r}"

		@tcr.force_keyword_only_typehints()
		async def anya(*, a: int, b) -> str:
			return f"async: {a!r}, {b!r}"

		c(nya(a=1, b=2))

		c(asyncio.run(anya(a=Eent(2), b=4)))

	def test_c_log_regression_no_newline():
		c.log("asfasdfas")
		c.log("12313241234")
		c.log("nyaaaa")
		c.log("uwuwuwuwu")
		c("asfasdfas")
		c("12313241234")
		c("nyaaaa")
		c("uwuwuwuwu")

	def test_timestr2_manual():
		from datetime import datetime

		from tcrutils.timestr2 import timestr as t_np
		from tcrutils.timestr2 import timestr_priority_adjusted as t
		from tcrutils.types import LiteralDisplay, PlainDisplay, QuotelessString

		tz = datetime.now().astimezone().tzinfo
		nowf = lambda tz=tz: datetime.now(tz=tz)

		seth = [
			"1h20m!13:",
			"13:!1h20m",
			"1h!13:",
			"wed!14:",
			"",
			"13:!!!!10m!!!5s",
			"",
			"13:",
			"13:!12:",
			"13:!13:",
			"13:!14:",
		]

		justamt = max(len(x) for x in seth)

		c([
			(
				PlainDisplay(
					LiteralDisplay(f"{k:>{justamt}}"),
					a := t.parse(k, tz=tz, _datetime_now=nowf),
					b := t_np.parse(k, tz=tz, _datetime_now=nowf),
					a == b,
					sep=" ",
				)
				if k != ""
				else LiteralDisplay(" " * (justamt + 39))
			)
			for k in seth
		])

	def test_sdb2():
		from tcrutils.sdb2 import ShelfManager

		DB_DIRECTORY = (p.Path(__file__).parent / "test_db2").absolute()
		DB_DIRECTORY.mkdir(exist_ok=True)

		global User

		class User(pydantic.BaseModel):
			model_config = pydantic.ConfigDict(
				validate_assignment=True,
				validate_default=True,
			)

			displayname: str = "uwu"
			number: int = 42

		class UserDB(ShelfManager[User]):
			PATH = DB_DIRECTORY / "users"

			def default_factory(self):
				return User()

		# with UserDB.open_shelf() as sh:
		# 	sh.clear()

		with UserDB.open_shelf() as sh:
			c(sh.keys())
			c(sh.values())
			c(sh.items())

		with UserDB(507642999992352779) as user:
			c(user)

		with UserDB.open_shelf() as sh:
			c(sh.keys())
			c(sh.values())
			c(sh.items())

		with UserDB(507642999992352779) as user:
			user.number += 1

		with UserDB.open_shelf() as sh:
			c(sh.keys())
			c(sh.values())
			c(sh.items())

		c(UserDB.contains(507642999992352779))
		c(UserDB.contains(507642999992352778))
		c(UserDB.contains("507642999992352779"))
		c(UserDB.contains("507642999992352778"))

	def test_sdb2_single():
		from tcrutils.sdb2 import SingleShelfManager

		DB_DIRECTORY = (p.Path(__file__).parent / "test_db2").absolute()
		DB_DIRECTORY.mkdir(exist_ok=True)

		global GlobalData

		class GlobalData(pydantic.BaseModel):
			model_config = pydantic.ConfigDict(
				validate_assignment=True,
				validate_default=True,
			)

			something: str = "global data something"
			eent: int = 69

		class GlobalDB(SingleShelfManager[GlobalData]):
			PATH = DB_DIRECTORY / "global"

			def default_factory(self):
				return GlobalData()

		with GlobalDB.open_shelf() as sh:
			sh.clear()

		with GlobalDB.open_shelf() as sh:
			c(sh.keys())
			c(sh.values())
			c(sh.items())

		with GlobalDB() as gd:
			c(gd)

		with GlobalDB.open_shelf() as sh:
			c(sh.keys())
			c(sh.values())
			c(sh.items())

	def test_dynamic_versioning():
		import tcrutils

		c("tcrutils.__version__ =", tcrutils.__version__)


if True:  # \/ # Test setup
	__TESTS_RAN_GLOBAL = 0

	def _count_tests_decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			global __TESTS_RAN_GLOBAL
			__TESTS_RAN_GLOBAL += 1
			return func(*args, **kwargs)

		return wrapper

	for k, v in globals().copy().items():  # Decorate each test_... function with the @tcr.test decorator
		if k.startswith("test_"):
			globals()[k] = test(_count_tests_decorator(v))

if __name__ == "__main__":
	test_print_iterable(
		_raise_errors=True,
		syntax_highlighting=1,
		# let_no_indent=0,
		# force_no_indent=1,
		# force_no_spaces=0,
		# force_complex_parenthesis=1,
		# item_limit=10,
		# # let_no_indent_max_non_iterables=10,
		# # let_no_indent_max_iterables=10,
		# prefer_full_names=1,
		# force_union_parenthesis=1,
		# depth_limit=3,
		# str_repr=repr,
	)

	# test_timestr()
	# test_dict_merge()
	# test_dict_zip()
	# test_oddeven()
	# test_timeit()
	# test_autorun()
	# test_breakpoint()
	# test_trei()
	# test_asert()
	# test_iterable(batched_=True, cut_at_=False)
	# test_path()
	# test_ifys()
	# test_print_iterable(print_iterable=print_iterable, syntax_highlighting=1)
	# test_print_iterable(print_iterable=lambda *args, **kwargs: print(tcr.fmt_iterable(*args, **kwargs)), syntax_highlighting=True)
	# test_print_iterable(print_iterable=print_iterable, syntax_highlighting=False)
	# test_markdown()
	# test_extract_error()
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
	# test_ass()
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
	# test_err_denoted()
	# test_is_snowflake()
	# test_console_fmt()
	# test_console_callsite()
	# test_console_callsite(c.with_expr_header(__name__, literal=True))
	# test_fucking_pydantic_model_dump_my_ass()
	# test_joke_pointer()
	# test_eval_fback()
	# test_console_with_header()
	# test_console_with_eval()
	# test_getch()
	# test_repl()
	# test_typehints()
	# test_c_log_regression_no_newline()
	# test_timestr2_manual()
	# test_sdb2()
	# test_sdb2_single()
	test_dynamic_versioning()

	print()
	_start_time__timeit_partial = TimeitPartial("*")
	_start_time__timeit_partial.t = _start_time
	_start_time__timeit_partial.stop()
	_start_time__timeit_partial.finish_and_print()
	del _start_time__timeit_partial, _start_time

	if not sys.gettrace():
		ass.total(prefix="\n")
		print()
		c("test# =", __TESTS_RAN_GLOBAL)
		pass  # noqa: PIE790, RUF100

if BOT:
	BOT.run()
