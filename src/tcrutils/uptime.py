import datetime


class UptimeResult:
	string: str
	"""Formatted string, for example: `10:20:30`"""
	total_seconds: int
	"""Total seconds, for example: 19234, For parsed seconds use `s`"""
	d: int
	"""Days"""
	h: int
	"""Hours"""
	m: int
	"""Minutes"""
	s: int
	"""Seconds, for total seconds use `total_seconds`"""
	delta: datetime.timedelta

	def __init__(
		self,
		*,
		string: str,
		total_seconds: int,
		d: int,
		h: int,
		m: int,
		s: int,
		delta: datetime.timedelta,
	) -> None:
		self.string = string
		self.total_seconds = total_seconds
		self.d = d
		self.h = h
		self.m = m
		self.s = s
		self.delta = delta

	def __int__(self) -> int:
		return self.total_seconds

	def __str__(self) -> str:
		return self.string


class Uptime:
	"""Counts time from when it's initialised. Returns as formatted str, datetime.delta, total_seconds or each number component (days, hours, minutes, seconds)."""

	def __init__(self) -> None:
		self.__start_time = datetime.datetime.now(tz=datetime.UTC)

	def get(self) -> UptimeResult:
		delta = datetime.datetime.now(tz=datetime.UTC) - self.__start_time
		total_seconds = delta.total_seconds()
		d = total_seconds // 86400
		h = (total_seconds // 3600) % 24
		m = (total_seconds // 60) % 60
		s = total_seconds % 60
		if d > 0:
			fmted = f"{int(d)}d + {int(h):02d}:{int(m):02d}:{int(s):02d}"
		else:
			fmted = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
		return UptimeResult(
			string=fmted,
			total_seconds=int(total_seconds),
			d=d,
			h=h,
			m=m,
			s=s,
			delta=delta,
		)

	def __str__(self) -> str:
		return str(self.get())

	def __int__(self) -> int:
		return int(self.get())
