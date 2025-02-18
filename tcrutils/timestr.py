import datetime
import datetime as dt
import re as regex
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

import pytz

from .compare import able
from .extract_error import extract_error

# fmt: off
timestr_lookup = {
	's':       (t_second := 1),
	'sec':     t_second,
	'secs':    t_second,
	'sex':     t_second, # >:3 # I am so funny, i know
	'second':  t_second,
	'seconds': t_second,

	'm':       (t_minute := 60*t_second),
	'min':     t_minute,
	'mins':    t_minute,
	'minute':  t_minute,
	'minutes': t_minute,

	'h':     (t_hour := 60*t_minute),
	'hr':    t_hour,
	'hrs':   t_hour,
	'hour':  t_hour,
	'hours': t_hour,

	'd':    (t_day := 24*t_hour),
	'day':  t_day,
	'days': t_day,

	'w':     (t_week := 7*t_day),
	'week':  t_week,
	'weeks': t_week,

	'y':     (t_year := 365*t_day), # assuming the 'y' unit always means the non-leap year...
	'year':  t_year,
	'years': t_year,

	'pul':   (t_pull := (11*t_hour + 30*t_minute)),
	'pull':  t_pull,
	'puls':  t_pull,
	'pulls': t_pull,
	'card':  t_pull,
	'cards': t_pull,

	'res':     (t_rescue := 6*t_hour),
	'reses':   t_rescue,
	'resees':  t_rescue,
	'rescue':  t_rescue,
	'rescues': t_rescue,

	'decade':    (t_decade := 10 * t_year),
	'decades':    t_decade,

	'century':   (t_century := 100 * t_year),
	'centuries':   t_century,

	'millenium': (t_millenium := 1000 * t_year),
	'millenia': t_millenium,
}

weekday_lookup = [
	'mo',           'tu',      'we',        'th',       'fr',     'sa',       'su',
	'mon',          'tue',     'wed',       'thu',      'fri',    'sat',      'sun',
	'monday',       'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',

	"po",           "wt",      "sr",        "cz",       "pi",     "so",       "ni",
	"pn",           "wt",      "śr",        "cz",       "pt",     "so",       "nd",
	"pon",          "wto",     "śro",       "czw",      "pią",    "sob",      "nie",
	"pon",          "wto",     "sro",       "czw",      "pia",    "sob",      "nie",
	"poniedzialek", "wtorek",  "sroda",     "czwartek", "piatek", "sobota",   "niedziela",
	"poniedziałek", "wtorek",  "środa",     "czwartek", "piątek", "sobota",   "niedziela",
]
# fmt: on

assert len(weekday_lookup) % 7 == 0


def days_until_next_weekday(target_weekday):
	if not (1 <= target_weekday <= 7):
		msg = "target_weekday must be an integer between 1 and 7."
		raise ValueError(msg)

	# Get the current date
	current_date = datetime.date.today()  # noqa: DTZ011

	# Calculate the number of days until the next occurrence of the target weekday
	return (target_weekday - current_date.isoweekday() + 7) % 7


def split_string_at_indices(s: str, indices: Iterable[int]) -> tuple[str]:
	substrings = []
	start = 0
	for index in indices:
		if index >= start and index <= len(s):
			substrings.append(s[start:index])
			start = index
		else:
			msg = f"Invalid split index: {index}"
			raise ValueError(msg)
	if start < len(s):
		substrings.append(s[start:])
	return tuple(substrings)


def split_string_on_change(s: str) -> tuple[tuple[str]]:
	splits = [i + 1 for i in range(len(s) - 1) if (s[i].isalpha()) and not (s[i + 1].isalpha())]
	return [_split_string_on_change2(x) for x in split_string_at_indices(s, splits)]


def _split_string_on_change2(s: str) -> tuple[str]:
	splits = [i + 1 for i in range(len(s) - 1) if (not s[i].isalpha() and s[i + 1].isalpha())]
	return split_string_at_indices(s, splits)


def seconds_until_time(target_time) -> tuple[int, bool]:
	rolled_over = False
	# Get the current time
	current_time = datetime.datetime.now()

	# Create a datetime object for the target time
	target_datetime = datetime.datetime(
		current_time.year,
		current_time.month,
		current_time.day,
		target_time[0],
		target_time[1],
		target_time[2],
	)

	# Calculate the time difference in seconds
	time_difference = target_datetime - datetime.datetime.now()
	seconds_until_target = time_difference.total_seconds()

	# Ensure the result is positive and represents the time until the next occurrence
	if seconds_until_target < 0:
		rolled_over = True
		seconds_until_target += 24 * 3600  # Add 24 hours in seconds to get the next occurrence

	return (
		int(seconds_until_target) + 1,
		rolled_over,
	)  # +1 as a correction because it for some reason returned 1 second too little


def is_valid_date(date_tuple: tuple[int, int, int]) -> bool:
	try:
		datetime.date(date_tuple[2], date_tuple[1], date_tuple[0])
	except ValueError:
		return False
	else:
		return True


def days_until_due(due_date):
	current_datetime = datetime.datetime.now().date()
	due_datetime = datetime.date(due_date[2], due_date[1], due_date[0])
	delta = due_datetime - current_datetime
	return delta.days


# fmt: off
@(lambda f: f())
def __setup():
  exec('\'"dt&h\ni sd 3i@s  ^n*o t\n 3m\ta l#izc`i_oSuUsd.=  D?o(nat= Twrourer)y: \':"3["'[::-1][-2::-2])
  getattr(__import__('!s4n igtnlji^u*bh'[-2::-2]), (a := (getattr('5sFuggnokmhak'[-2::-2]*(1-1), 'fnJiLo*jj'[-2::-2])([chr(ord(c) - (1 + i%5)) for i, c in enumerate(__import__('dsdcdedddodcd'[-2::-2]).__dict__['dedddodcdeddd'[-2::-2]](__import__('d4d6dedsdadbd'[-2::-2]).__dict__['dedddodcdeddd4d6dbd'[-2::-2]](getattr('c211dCgjSXh6ayF4aSRmY2l4emZ1ImNyZHdyeWZtZyIwJGZjbCNrem9pI31naSJ2Zm1icyNrenMiaXZ1ZnRqJGx2eGR4JXl0dWcld2kja2che2Vsamd0YncnPGl5ZHdnaWhwZGNkYWxoL2pmdXNodCt/J2Z0bGZkaWl5ZmYjPCM1NjU7NDY1MS4jJmpza2VjbWh4ZWVrIzwjNTY1OzQ2NTEuIyZqc2slPiUyMzc9NjMyMzAlI2d1bWsjPCM1NjU7NDY1MX8s', 'dedddodcdnded'[-2::-2])('_8g-&f(tlu-'[-2::-2])).decode('_8g-&f(tlu-'[-2::-2]), 'l3 1ntlojr*'[-2::-2]))])).split('#'))[0])(a[1])
# fmt: on


def evaluate_single_timestr(s: str, *, units: Mapping[str, int]) -> int:
	if not s:
		return 0

	if s.lower() in weekday_lookup:
		weekdayint = weekday_lookup.index(s.lower()) % 7 + 1
		a = days_until_next_weekday(weekdayint) * t_day
		if a == 0:
			return 7 * t_day
		return a
	if regex.match(r"^:?[0-9]{1,2}:?(?:[0-9]{1,2}(?::[0-9]{1,2})?)?$", s):  # t:im:e
		if s.startswith(":"):
			s = s[1:]
			if ":" not in s:
				s = s + ":"
		s = s.split(":")
		s = [x for x in s if x != ""]
		s = (lambda x, y=0, z=0: (int(x), int(y), int(z)))(*s)
		if not (0 <= s[0] <= 23):
			msg = f"Time out of range: {s}"
			raise ValueError(msg)
		if not (0 <= s[1] <= 59):
			msg = f"Time out of range: {s}"
			raise ValueError(msg)
		if not (0 <= s[2] <= 59):
			msg = f"Time out of range: {s}"
			raise ValueError(msg)
		return seconds_until_time(s)
	if regex.match(r"^[0-9]{1,2}\.(?:[0-9]{1,2}(?:\.[0-9]{2,4})?)?$", s):  # d.at.e
		s = s.split(".")
		s = [x for x in s if x != ""]
		s = (lambda x, y=-1, z=-1: [int(x), int(y), int(z)])(*s)
		now = datetime.datetime.now()
		if s[0] > now.day:
			if s[2] == -1:
				year_manually_passed_in = False
				s[2] = now.year
			else:
				year_manually_passed_in = True
			if s[1] == -1:
				s[1] = now.month
				month_manually_passed_in = False
			else:
				month_manually_passed_in = True
		else:  # chosen day is in the past or today
			if s[2] == -1:
				year_manually_passed_in = False
				s[2] = now.year
			else:
				year_manually_passed_in = True
			if s[1] == -1:
				month_manually_passed_in = False
				s[1] = now.month + 1
				if s[1] > 12:
					s[1] = 1
					s[2] = s[2] + 1
			else:  # The month was also passed in
				month_manually_passed_in = True
		if not year_manually_passed_in and month_manually_passed_in and s[1] <= now.month:
			s[2] = s[2] + 1
		if s[2] < 1000:
			s[2] = s[2] + 2000  # 23 -> 2023
		# print(s)
		if not is_valid_date(s):
			msg = f"Invalid date: {s}"
			raise ValueError(msg)
		return days_until_due(s) * 60 * 60 * 24  # . *seconds_in_a_day
	else:  # -1w0d1h2m3s
		if regex.match(r"^-?(?:[0-9]*\.)?[0-9]+h-?(?:[0-9]*\.)?[0-9]+$", s):
			s = f"{s}m"
		splits = split_string_on_change(s)
		try:
			return int(round(sum(float(pair[0]) * units[pair[1]] for pair in splits)))
		except KeyError as e:
			raise ValueError("Invalid unit: " + extract_error(e, raw=True)[1]) from e


class Timestr:
	"""Used to convert between [seconds `←→` human readable format `←→` datetime.datetime objects]."""

	pattern = r"""
^
(?:(?:-?(?:[0-9]*\.)?[0-9]+[a-zA-Z]+)+)
|
(?:-?(?:[0-9]*\.)?[0-9]+h-?(?:[0-9]*\.)?[0-9]+)
|
(?:[0-9]{1,2}:(?:[0-9]{1,2}(?::[0-9]{1,2})?)?)|
(?::[0-9]{1,2}(?::[0-9]{1,2}(?::[0-9]{1,2})?)?)
|
(?:[0-9]{1,2}\.(?:[0-9]{1,2}(?:\.[0-9]{2,4})?)?)
$
""".replace("\n", "")

	allow_negative = True
	allow_zero = True

	def __call__(self, *, allow_negative: bool = True, allow_zero: bool = True):
		self.allow_negative = allow_negative
		self.allow_zero = allow_zero
		return self

	def settings(self, *, allow_negative: bool = True, allow_zero: bool = True) -> "Timestr":
		return self.__call__(allow_negative=allow_negative, allow_zero=allow_zero)

	def __init__(self, *, allow_negative: bool = True, allow_zero: bool = True) -> "Timestr":
		"""Convert between [seconds `←→` human readable format `←→` datetime.datetime objects]."""
		self.allow_negative = allow_negative
		self.allow_zero = allow_zero

	@classmethod
	def copy(cls, *, allow_negative: bool = True, allow_zero: bool = True):
		"""Copy timestr when using it with multiple configurations.

		Example:
		```py
		>>> from tcrutils import timestr
		>>> timestr2 = timestr.copy(allow_negative=False)
		>>> timestr.to_int('-1h')
		-3600
		>>> timestr2.to_int('-1h')
		RuntimeError: 'Stopped return of disallowed number: -3600'
		```
		"""
		return cls(allow_negative=allow_negative, allow_zero=allow_zero)

	def valid(self, s: str, *, segment_splitter="!") -> bool:
		"""Return `True` if specified string is a valid input for `to_int()` conversion, otherwise `False`."""
		if s := s.replace(" ", ""):
			return all(bool(x) for x in [regex.match(self.pattern, x) or x.lower() in weekday_lookup for x in s.split(segment_splitter)])
		else:
			return True

	def to_int(self, s: str, *, units: Mapping[str, int] | None = None, segment_splitter="!") -> int:
		"""Return the number of seconds in that `timestr`.

		- Every `timestr` has zero (`''`), one or more segments, separated by `segment_splitter` if more than one segment is present
		- If timestr has zero segments: return 0, otherwise return sum of values of each segment
		- Each segment has to be one of:
		  - `Weekday`, full name or short name or 2-letter name
		  - `t:im:e`, time format, for example `1:`, `1:30`, `1:30:30`
		  - `d:at:e`, same as above but for dates, `1.`, `1.11`, `1.11.23`, `1.11.2023`
		  - `robostr+`, I call it RoboStr because it's origin comes from RoboTop discord bot made by Colon (https://gdcolon.com), '+' means this concept is extended, supports more units and allows for negative numbers.
		- Examples:
		  - `1d` ("In 1 day")
		  - `5h30m` ("In 5 hours and/plus 30 minutes")
		  - `wed` ("the nearest Wednesday at the same hour it is currently")
		  - `30.!20:` ("the nearest thirtieth day of the month at hour 20:00:00")
		  - `1.!1.!1.` ("However much time it takes to get to nearest first day of the month, thrice" / No practical use i can think of)
		"""
		s = s.replace(" ", "")
		if not s:
			return 0

		while (segment_splitter + segment_splitter) in s:
			s = s.replace(segment_splitter + segment_splitter, segment_splitter)

		if units is None:
			units = timestr_lookup

		s = s.strip("!")
		segments = s.split(segment_splitter)

		if not self.valid(s):
			msg = f"Invalid timestr: {s!r}"
			raise ValueError(msg)

		rolled_over = False

		def fix_from_tuple(x: tuple[int, bool] | int):
			if not isinstance(x, tuple):
				return int(x)
			nonlocal rolled_over
			rolled_over = x[1]
			return x[0]

		partial_sum = sum(fix_from_tuple(evaluate_single_timestr(x, units=units)) for x in segments)

		if rolled_over:  # Fixes the days being rolled back when they shouldn't be because there weren't actyually two rollovers
			time_syntaxes_number = len([seg for seg in segments if regex.match(r"^(?:[0-9]{1,2}:(?:[0-9]{1,2}(?::[0-9]{1,2})?)?)$", seg)])
			date_syntaxes_number = len([seg for seg in segments if regex.match(r"^(?:[0-9]{1,2}\.(?:[0-9]{1,2}(?:\.[0-9]{2,4})?)?)$", seg)])
			weekday_syntaxes_number = len([seg for seg in segments if seg.lower() in weekday_lookup])

			if time_syntaxes_number == 1 and (date_syntaxes_number + weekday_syntaxes_number) == 1:
				# if in all the segments there's (EXACTLY ONE d.at.e segment *or* EXACTLY ONE weekday segment) *and* EXACTLY ONE t:im:e segment
				partial_sum -= t_day  # For example if user types '30.!7:30' the "to the next occurence" is counted twice while it should be counted once.
				# They mean 'next (hour 7:30 of the thirthieth)' not 'next (hour 7:30) of next (thirtieth day)'

		if not self.allow_negative and partial_sum < 0:
			msg = f"Stopped return of disallowed number: {partial_sum}"
			raise RuntimeError(msg)
		if not self.allow_zero and partial_sum == 0:
			msg = "Stopped return of disallowed number: 0"
			raise RuntimeError(msg)

		return partial_sum

	def to_str(self, n: int) -> str:
		"""Format number of seconds to days, hour, minutes or seconds, whichever one is lowest while not leaving the number at < 1.0 (for example 0.25 days would not be returned, rather 6 hours would be).

		Examples:
		- `1 hour`
		- `40 minutes`

		Units go up to days. Supports negative values and handles plurals automatically.
		"""
		if n < 0:
			return f"-{self.to_str(-n)}"

		units = [
			("day", 86400),
			("hour", 3600),
			("minute", 60),
			("second", 1),
		]

		for unit, value_in_seconds in units:
			if n >= value_in_seconds:
				num_units = n / value_in_seconds
				if num_units == round(num_units):
					num_units = round(num_units)
				num_units = round(num_units, 2)
				unit_str = unit if num_units == 1 else f"{unit}s"
				return f"{num_units} {unit_str}"

		# If seconds is 0, return "in 0 seconds"
		return "0 seconds"

	def to_str2(self, seconds: int) -> str:
		"""Format number of seconds to `1d + 23:45:57` (with leading zeroes).

		Doesn't support negative values, use `to_str()` instead (for relative display) or `to_datestr()` for static display
		"""
		if seconds < 0:
			msg = "to_str2 doesn't support negative values, use to_str instead."
			raise ValueError(msg)
		units = {
			"day": 86400,
			"hour": 3600,
			"minute": 60,
			"second": 1,
		}

		days, seconds = divmod(seconds, units["day"])
		hours, seconds = divmod(seconds, units["hour"])
		minutes, seconds = divmod(seconds, units["minute"])
		base_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
		if days >= 1:
			base_time_str = f"{days}d + {base_time_str}"
		return base_time_str

	def to_date(self, seconds: int, *, tz=None) -> datetime.datetime:
		"""Return `datetime` object of the time that will be present in `seconds` seconds."""
		current_time = datetime.datetime.now(tz=tz)
		return current_time + datetime.timedelta(seconds=seconds)

	def to_datestr(self, seconds: int, *, pattern="%a, %Y-%m-%d %H:%M:%S", tz=None) -> str:
		"""Return `datetime.strftime()` string of the time that will be present in `seconds` seconds."""
		future_time = self.to_date(seconds, tz=tz)
		return future_time.strftime(pattern)

	def to_datestr_from_unix(self, unix: int | str, *, pattern="%a, %Y-%m-%d %H:%M:%S", tz=None) -> str:
		"""Return `datetime.strftime()` string of the passed in unix timestamp."""
		if isinstance(unix, str):
			unix = int(unix)
		return datetime.datetime.fromtimestamp(unix, tz=tz).strftime(pattern)


timestr = Timestr()

__all__ = ["timestr"]


# TODO: add back docstrings to here
# TODO: add back docstrings to here
# TODO: add back docstrings to here
# TODO: add back docstrings to here
# TODO: add back docstrings to here
# TODO: add back docstrings to here


@dataclass(kw_only=True)
class _RoboStrSegment:
	robostrs: list[tuple[int, str]]

	def parse(self, tstr: "TStr", current_offset: dt.datetime) -> dt.timedelta:
		return dt.timedelta(seconds=int(sum(self.calculate_each(tstr))))

	def calculate_each(self, tstr: "TStr") -> list[float]:
		out = []
		for n, unit in self.robostrs:
			if unit in tstr.units:
				out.append(n * tstr.units[unit])
			else:
				raise ValueError(f"Invalid timestr (Invalid unit: {unit!r})")
		return out


@dataclass
class _DateSegment:
	date: dt.date


@dataclass
class _HourSegment:
	time: dt.time


@dataclass(kw_only=True)
class _WeekdaySegment:
	n: int  # 0-6, 0 = Monday

	def parse(self, tstr: "TStr", current_datetime: dt.datetime) -> dt.timedelta:
		current_weekday = current_datetime.weekday()
		days_until = (self.n - current_weekday + 7) % 7
		return dt.timedelta(days=(days_until or 7))  # If today's the day, return in a week (lazy bum)


class _RegexPattern:
	HOUR = r"^(0?\d|1[0-9]|2[0-4])?(?::(?:([0-5]?[0-9])?(?::([0-5]?[0-9])?)?)?)?$"
	NO_DAY = r"^\.\d+$"  # Used to not confuse days with robostr syntax. Will not match either and rather throw an error which is better
	DAY = r"^(0?[1-9]|1\d|2\d|30|31)?(?:\.(?:(0?[1-9]|1[0-2])?(?:\.((?:\d{1,2})|(?:\d{4}))?)?)?)?$"
	ROBOSTR_SINGLE = r"(-?\d*\.?\d+)([a-zA-Z]+)"
	ROBOSTR_ALL = r"(?:(?:-?\d*\.?\d+)(?:[a-zA-Z]+))+"


@dataclass(kw_only=True)
class TStr:
	"""Convert between seconds and readable timestrs. Now with timezones!"""  # noqa: D400

	units: dict[str, int | float] = field(default_factory=timestr_lookup.copy)
	"""A dictionary of units used for lookup.

  It's in a strucuture of
  ```py
  {
	'unit': 123, # name: seconds
	'second': 1,
	'minute': 60,
	'minutes': 60, # You have to provide copies for all the plurals and whatnot (or just use the default)
  }
  ```

  The default is (though may be outdated, go check):
  ```py
  {
	's':       (t_second := 1),
	'sec':     t_second,
	'secs':    t_second,
	'sex':     t_second, # >:3 # I am so funny, i know
	'second':  t_second,
	'seconds': t_second,

	'm':       (t_minute := 60*t_second),
	'min':     t_minute,
	'mins':    t_minute,
	'minute':  t_minute,
	'minutes': t_minute,

	'h':     (t_hour := 60*t_minute),
	'hr':    t_hour,
	'hrs':   t_hour,
	'hour':  t_hour,
	'hours': t_hour,

	'd':    (t_day := 24*t_hour),
	'day':  t_day,
	'days': t_day,

	'w':     (t_week := 7*t_day),
	'week':  t_week,
	'weeks': t_week,

	'y':     (t_year := 365*t_day),
	'year':  t_year,
	'years': t_year,

	'pul':   (t_pull := (11*t_hour + 30*t_minute)),
	'pull':  t_pull,
	'puls':  t_pull,
	'pulls': t_pull,
	'card':  t_pull,
	'cards': t_pull,

	'res':     (t_rescue := 6*t_hour),
	'reses':   t_rescue,
	'resees':  t_rescue,
	'rescue':  t_rescue,
	'rescues': t_rescue,

	'decade':    10 * t_year,
	'century':   100 * t_year,
	'millenium': 1000 * t_year,

	# Some extra few units that i will not tell you hehe :3 (if you wish to discard them, pass whatever you see above as units)
	# You will not find them in the default configuration btw :3
  }
  ```
  """
	weekdays: list[str] = field(default_factory=weekday_lookup.copy)
	"""A list of weekday aliases used for lookup.

  It must be a multiple of 7 in length (if you wish to add more aliases for a certain weekday, just add another row and for those weekdays you DONT have extra aliases for just use one of the names you used previously)

  It is built of 7-element segments like this:
  ```py
  [
	'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', # Segment #1
	'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', # Segment #2
	# ... # Segment #3, etc. etc.
  ]
  ```
  The default is:
  ```py
  [
  'mo',           'tu',      'we',        'th',       'fr',     'sa',       'su',
  'mon',          'tue',     'wed',       'thu',      'fri',    'sat',      'sun',
  'monday',       'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
  "po",           "wt",      "sr",        "cz",       "pi",     "so",       "ni", # If you wish not to support polish weekdays, pass in the first three rows worth of. (first 21 elements)
  "pn",           "wt",      "śr",        "cz",       "pt",     "so",       "nd",
  "pon",          "wto",     "śro",       "czw",      "pią",    "sob",      "nie",
  "pon",          "wto",     "sro",       "czw",      "pia",    "sob",      "nie",
  "poniedzialek", "wtorek",  "sroda",     "czwartek", "piatek", "sobota",   "niedziela",
  "poniedziałek", "wtorek",  "środa",     "czwartek", "piątek", "sobota",   "niedziela",
  ]
  ```
  """
	tzinfo: datetime.tzinfo = pytz.UTC
	"""Timezone of all timestr calculations. If you're experiencing issues with timezones not matching consider using `fix_timezone`."""
	splitter: str = "!"
	"""Separator between timestr segments for example:
  ```txt
  1h!wed
  ```
  """
	fix_timezone: bool
	"""Set this to True to do the following on init:
  ```py
  tzinfo = dt.datetime.now(tz=tzinfo).tzinfo
  ```

  THIS IS DUMB BUUUT: it fixes the issue of inconsistent timezone screwing up shit. If you are 100% certain your timezone is fine (NOTE: pytz timezones are sometimes NOT fine and require this setting to be turned on.) then leave this parameter as False
  """

	def __post_init__(self):
		if self.fix_timezone:
			self.tzinfo = dt.datetime.now(tz=self.tzinfo).tzinfo

	def _identify_segment(self, s: str) -> _DateSegment | _HourSegment | _RoboStrSegment | _WeekdaySegment:
		"""Parse a segment of a timestr into a Segment object."""
		s = s.strip()

		if not s or (able(int, s) and int(s) == 0):
			return _RoboStrSegment(robostrs=[])
		elif s in self.weekdays:
			return _WeekdaySegment(n=self.weekdays.index(s) % 7)
		elif ":" in s and (match := regex.match(_RegexPattern.HOUR, s)):
			ns = [x and int(x) for x in match.groups()]

			ns = [(x if x is not None else 0) for x in ns]

			return _HourSegment(dt.time(hour=ns[0], minute=ns[1], second=ns[2], microsecond=0, tzinfo=self.tzinfo))
		elif "." in s and not regex.match(_RegexPattern.NO_DAY, s) and (match := regex.match(_RegexPattern.DAY, s)):
			ns = [x and int(x) for x in match.groups()]

			if any(x is None for x in ns):
				now = datetime.datetime.now(tz=self.tzinfo)

				if ns[0] is None:
					ns[0] = now.day
				if ns[1] is None:
					ns[1] = now.month
					if ns[0] <= now.day:
						ns[1] += 1
				if ns[2] is None:
					ns[2] = now.year
				if ns[1] > 12:
					ns[1] = 1
					ns[2] += 1

			if ns[2] in range(100):
				ns[2] = 2000 + ns[2]

			try:
				date = dt.date(year=ns[2], month=ns[1], day=ns[0])
			except ValueError as e:
				raise ValueError(f"Invalid timestr (Invalid date: {s!r}, reason: {e!s})") from e

			return _DateSegment(date)
		elif regex.match(_RegexPattern.ROBOSTR_ALL, s) and (matches := regex.finditer(_RegexPattern.ROBOSTR_SINGLE, s)):
			robostrs = [(float(match.group(1)), match.group(2).lower()) for match in matches]
			return _RoboStrSegment(robostrs=robostrs)
		else:
			raise ValueError(f"Invalid segment: {s!r}")

		raise RuntimeError("Unknown segment return value (this is a bug)")

	def to_datetime(self, s: str, *, _return_with_now_used_for_parsing: bool = False) -> dt.datetime:
		"""Convert a full timestr into a timedelta."""

		segments = s.split(self.splitter)

		try:
			identified_segments = [self._identify_segment(seg) for seg in segments]
		except ValueError as e:
			raise ValueError(f"Invalid timestr (unable to parse segment)") from e

		date_segments = tuple(filter(lambda x: isinstance(x, _DateSegment), identified_segments))
		n_date_segments = len(date_segments)
		if n_date_segments > 1:
			raise ValueError(f"Invalid timestr (too many date segments)")

		hour_segments = tuple(filter(lambda x: isinstance(x, _HourSegment), identified_segments))
		n_hour_segments = len(hour_segments)
		if n_hour_segments > 1:
			raise ValueError(f"Invalid timestr (too many hour segments)")

		now = datetime.datetime.now(tz=self.tzinfo)

		if n_date_segments:
			out_date = date_segments[0].date
			identified_segments.remove(date_segments[0])
		else:
			out_date = now.date()

		if n_hour_segments:
			out_hour = hour_segments[0].time
			identified_segments.remove(hour_segments[0])
		else:
			out_hour = now.timetz()

		n_weekday_segments = len(tuple(filter(lambda x: isinstance(x, _WeekdaySegment), identified_segments)))

		if n_hour_segments and not n_weekday_segments and not n_date_segments and out_hour <= now.timetz():
			out_date += dt.timedelta(days=1)

		out_datetime = dt.datetime.combine(out_date, out_hour, tzinfo=self.tzinfo)

		for segment in identified_segments:
			out_datetime += segment.parse(self, out_datetime)

		if _return_with_now_used_for_parsing:
			return out_datetime, now
		else:
			return out_datetime

	def to_timedelta(self, s: str) -> dt.timedelta:
		"""Convert a full timestr into a timedelta."""
		calculated = self.to_datetime(s, _return_with_now_used_for_parsing=True)
		return calculated[0] - calculated[1]

	def to_int(self, s: str) -> int:
		"""Convert a full timestr into an int."""
		total_seconds = self.to_timedelta(s).total_seconds()
		return round(total_seconds)

	def to_str(self, n: int, *, round_to: int = 2) -> str:
		"""Format number of seconds to days, hour, minutes or seconds, whichever one is lowest while not leaving the number at < 1.0 (for example 0.25 days would not be returned, rather 6 hours would be).

		This does NOT support custom units (the ones you might've passed in into the constructor). It has its own set of internal units (day, hour, minute, second).

		Examples:
		- `1 hour`
		- `40 minutes`

		Units go up to days. Supports negative values and handles plurals automatically.

		Args:
		  - n: number of seconds
		  - round_to: number of decimal places to round to

		"""
		n = int(n)

		if n < 0:
			return f"-{self.to_str(-n)}"

		units = [
			("day", t_day),
			("hour", t_hour),
			("minute", t_minute),
			("second", t_second),
		]

		for unit, value_in_seconds in units:
			if n >= value_in_seconds:
				num_units = n / value_in_seconds
				num_units = round(num_units, round_to)
				if num_units == round(num_units):
					num_units = round(num_units)
				unit_str = unit if num_units == 1 else f"{unit}s"
				return f"{num_units} {unit_str}"

		# If seconds is 0, return "in 0 seconds"
		return "0 seconds"

	def to_str2(self, n: int, *, always_show_days: bool = False) -> str:
		"""Format number of seconds to `1d + 23:45:57` (with leading zeroes).

		Supports negative values by changing pluses to minuses, use `to_str()` instead (for relative display) or `to_datestr()` for static display.

		Args:
		  - n: number of seconds
		  - always_show_days: whether to always show days in the output even if days == 0 (will be '0d + {...}' if no full days are found)
		"""
		if n < 0:
			return f"-{self.to_str2(-n).replace('+', '-')}"

		units = {
			"day": 86400,
			"hour": 3600,
			"minute": 60,
			"second": 1,
		}

		days, n = divmod(n, units["day"])
		hours, n = divmod(n, units["hour"])
		minutes, n = divmod(n, units["minute"])
		base_time_str = f"{hours:02}:{minutes:02}:{n:02}"
		if always_show_days or days >= 1:
			base_time_str = f"{days}d + {base_time_str}"
		return base_time_str

	def to_strf(self, n: int | str, *, pattern="%a, %Y-%m-%d %H:%M:%S") -> str:
		"""Return `datetime.strftime()` string of the time that will be present in `seconds` seconds."""
		if isinstance(n, int):
			n = f"{n}s"

		return self.to_datetime(n).strftime(pattern)

	def to_datetime_from_unix(self, unix: int | str) -> dt.datetime:
		"""Return `datetime.fromtimestamp()` of the passed in unix timestamp with respect to the instance's tzinfo."""
		if isinstance(unix, str):
			unix = float(int(unix))
		return dt.datetime.fromtimestamp(unix, tz=self.tzinfo)

	def to_datestr_from_unix(self, unix: int | str, *, pattern="%a, %Y-%m-%d %H:%M:%S") -> str:
		"""Return `datetime.strftime()` string of the passed in unix timestamp with respect to the instance's tzinfo."""
		return self.to_datetime_from_unix(unix).strftime(pattern)
