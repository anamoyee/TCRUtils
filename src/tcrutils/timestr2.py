from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from datetime import tzinfo as _TzInfo
from typing import Self


class Segment(ABC):
	priority: int = 0
	"""## Higher value `=` applied earlier (NOT try_parsed earlier, try_parsing is dependant on the order of Parser.segment_types: tuple[type[Segment]])"""

	@classmethod
	@abstractmethod
	def try_parse(cls, text: str, /) -> Self | None:
		"""Attempt to parse the given text as this segment type. Return an instance if successful, or None otherwise."""

	@abstractmethod
	def apply(self, dt: datetime, now: datetime, segments: list[Segment], /) -> datetime:
		"""Apply this segment to the datetime dt and return the new datetime."""


class DateSegment(Segment):
	priority = 20

	DATE_REGEX = re.compile(r"^(?P<day>\d{1,2})-" r"(?P<month>\d{1,2})?" r"(?:-(?P<year>\d{1,4})?)?$")

	def __init__(self, day: int, month: int | None, year: int | None):
		self.day = day
		self.month = month
		self.year = year

	@classmethod
	def try_parse(cls, text: str, /) -> Self | None:
		m = cls.DATE_REGEX.fullmatch(text)
		if not m:
			return None

		day = int(m.group("day"))
		month_str = m.group("month")
		year_str = m.group("year")
		month = int(month_str) if month_str and month_str != "" else None
		year = int(year_str) if year_str and year_str != "" else None
		return cls(day, month, year)

	def apply(self, dt: datetime, now: datetime, segments: list[Segment], /) -> datetime:
		try:
			additional_years = 0
			additional_months = 0

			tries = 10

			while 1:
				if additional_months > 12:
					additional_months -= 12
					additional_years += 1

				try:
					dt = dt.replace(
						year=(self.year if self.year is not None else dt.year) + additional_years,
						month=(self.month if self.month is not None else dt.month) + additional_months,
						day=self.day,
					)

					break
				except ValueError as e:
					if str(e) != "day is out of range for month" and self.day <= 31:
						raise

					tries -= 1
					if tries <= 0:
						raise

					if self.month is not None and self.year is not None:
						raise

					if self.month is None:
						additional_months += 1
						continue

					additional_years += 1
					continue

			if self.month is not None and self.year is not None:
				return dt

			if self.month is not None:
				while dt <= now:
					dt = dt.replace(year=dt.year + 1)

				return dt

			while dt <= now:
				new_month = dt.month + 1
				new_year = dt.year

				if new_month > 12:
					new_month -= 12
					new_year += 1

				dt = dt.replace(month=new_month, year=new_year)

			return dt  # noqa: TRY300

		except ValueError as e:
			raise ValueError(f"Invalid date while applying date segment: {self}") from e

	def __repr__(self):
		return f"DateSegment(day={self.day}, month={self.month}, year={self.year})"


class TimeSegment(Segment):
	priority = 10

	TIME_REGEX = re.compile(r"^(?P<hour>\d{1,2}):" r"(?P<minute>\d{1,2})?" r"(?:\:(?P<second>\d{1,2})?)?$")

	def __init__(self, hour: int, minute: int, second: int):
		self.hour = hour
		self.minute = minute
		self.second = second

	@classmethod
	def try_parse(cls, text: str, /) -> Self | None:
		m = cls.TIME_REGEX.fullmatch(text)
		if not m:
			return None
		hour_str = m.group("hour")
		minute_str = m.group("minute")
		second_str = m.group("second")
		hour = int(hour_str) if hour_str != "" else 0
		minute = int(minute_str) if (minute_str is not None and minute_str != "") else 0
		second = int(second_str) if (second_str is not None and second_str != "") else 0

		if not (0 <= hour <= 23):
			raise ValueError("Hour must be in 0-23")
		if not (0 <= minute <= 59):
			raise ValueError("Minute must be in 0-59")
		if not (0 <= second <= 59):
			raise ValueError("Second must be in 0-59")
		return cls(hour, minute, second)

	def apply(self, dt: datetime, now: datetime, segments: list[Segment], /) -> datetime:
		before = dt

		try:
			dt = dt.replace(hour=self.hour, minute=self.minute, second=self.second, microsecond=0)
		except ValueError as e:
			raise ValueError("Invalid time after applying time segment") from e

		if not any(isinstance(segment, DateSegment | WeekdaySegment) for segment in segments):
			if dt <= before:
				dt = dt + timedelta(days=1)

		return dt

	def __repr__(self):
		return f"TimeSegment(hour={self.hour}, minute={self.minute}, second={self.second})"


class WeekdaySegment(Segment):
	priority = 15

	# fmt: off
	WEEKDAYS = [
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

	def __init__(self, weekday: int):
		self.weekday = weekday

	@classmethod
	def try_parse(cls, text: str, /) -> Self | None:
		key = text.lower()
		if key in cls.WEEKDAYS:
			return cls(cls.WEEKDAYS.index(key) % 7)
		return None

	def apply(self, dt: datetime, now: datetime, segments: list[Segment], /) -> datetime:
		current_weekday = dt.weekday()
		days_ahead = (self.weekday - current_weekday) % 7
		if days_ahead == 0:
			days_ahead = 7  # always jump forward at least one week if already on that day
		return dt + timedelta(days=days_ahead)

	def __repr__(self):
		return f"WeekdaySegment(weekday={self.weekday})"


class RobostrSegment(Segment):
	PAIR_REGEX = re.compile(r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))([a-zA-Z]+)")

	# fmt: off
	UNITS = {
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
	}
	# fmt: on

	def __init__(self, seconds: float):
		self.seconds = seconds

	@classmethod
	def try_parse(cls, text: str, /) -> Self | None:
		total = 0.0
		pos = 0
		for m in cls.PAIR_REGEX.finditer(text):
			if m.start() != pos:
				return None
			num_str = m.group(1)
			unit_str = m.group(2).lower()
			try:
				value = float(num_str)
			except ValueError as e:
				raise ValueError(f"Invalid number in robostr segment: {num_str}") from e
			if unit_str not in cls.UNITS:
				raise ValueError(f"Unknown unit '{unit_str}' in robostr segment")
			total += value * cls.UNITS[unit_str]
			pos = m.end()
		if pos != len(text) or pos == 0:
			return None
		return cls(total)

	def apply(self, dt: datetime, now: datetime, segments: list[Segment], /) -> datetime:
		return dt + timedelta(seconds=self.seconds)

	def __repr__(self):
		return f"RobostrSegment(seconds={self.seconds})"


class TimestrParser:
	segment_types: tuple[type[Segment]]
	respect_segment_priority: bool
	priorty_overrides: dict[type[Segment], int]

	def __init__(self, *segment_types: type[Segment], respect_segment_priority: bool = True, priority_overrides: dict[type[Segment], int] = None):
		self.segment_types = segment_types
		self.respect_segment_priority = respect_segment_priority
		self.priorty_overrides = priority_overrides if priority_overrides is not None else {}

	def parse(self, input_str: str, tz: timezone = datetime.now().astimezone().tzinfo, *, _datetime_now: Callable[[_TzInfo], datetime] = datetime.now) -> datetime:
		"""Given an input string (e.g. "1h20m!13:") and a timezone, return a datetime representing the datetime after now(tz=tz) + the amount of deltatime stored as segments in the input_str.

		The input string is processed as follows:
			1. Remove all spaces and split by '!'
			2. try_parse each segment (weekday, date, time, or robostr by default)
				- In the order they were passed to the parser's __init__
			3. Starting from now (with timezone tz), apply the segments by their priority from highest to lowest, by default it's:
				- date segments (if any; missing parts are inherited from now),
				- weekday segments (jumping forward to the next occurrence, even if landed spot-on),
				- time segments (missing pieces default to 0, eg. 13: -> 13:00:00, 13:45 -> 13:45:00),
				- robostr segments (adding a relative offset).
		"""
		cleaned = input_str.replace(" ", "")
		parts = [part for part in cleaned.split("!") if part != ""]

		all_segments: list[Segment] = []

		for part in parts:
			seg = None
			for seg_class in self.segment_types:
				candidate = seg_class.try_parse(part)
				if candidate is not None:
					seg = candidate
					break
			if seg is None:
				raise ValueError(f"Unrecognized segment: {part}")

			all_segments.append(seg)

		root_dt = now_dt = _datetime_now(tz).replace(microsecond=0)

		if self.respect_segment_priority:
			all_segments_priority_adjusted = sorted(all_segments, key=lambda seg: self.priorty_overrides.get(type(seg), seg.priority), reverse=True)
		else:
			all_segments_priority_adjusted = all_segments

		for seg in all_segments_priority_adjusted:
			root_dt = seg.apply(root_dt, now_dt, all_segments)

		return root_dt


SEGMENTS = (WeekdaySegment, DateSegment, TimeSegment, RobostrSegment)

timestr_priority_adjusted = TimestrParser(*SEGMENTS)
timestr = TimestrParser(*SEGMENTS, respect_segment_priority=False)
