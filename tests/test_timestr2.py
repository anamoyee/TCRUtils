from datetime import date, datetime, time
from datetime import timedelta as Δ
from datetime import tzinfo as _TzInfo
from functools import partial
from types import EllipsisType

import pytest
from tcrutils.console import c
from tcrutils.decorator import copy_kwargs
from tcrutils.timestr2 import timestr as t

tz = datetime.now().astimezone().tzinfo


if True:  # Fixtures

	@pytest.fixture()
	def true_now():
		return now_tz_μ0()


if True:  # Helpers

	def now_tz_μ0():
		return datetime.now(tz=tz).replace(microsecond=0)

	def eq_datetime(
		a: datetime,
		b: datetime,
		*,
		tolerance: Δ = Δ(seconds=0),
		print_=True,
	):
		if print_:
			print()
			c("a=", a)
			c("b=", b)

		diff = abs(a - b)

		if print_:
			c("diff=", diff)

		result = diff <= tolerance

		if not result:
			c.error("not result!")

		return result

	def datetime_dict(dt: datetime):
		return {
			"year": dt.year,
			"month": dt.month,
			"day": dt.day,
			"hour": dt.hour,
			"minute": dt.minute,
			"second": dt.second,
			"microsecond": dt.microsecond,
			"tz": dt.tzinfo,
		}

	@copy_kwargs
	def mdtn_factory(
		*,
		year: int | EllipsisType = ...,
		month: int | EllipsisType = ...,
		day: int | EllipsisType = ...,
		hour: int | EllipsisType = ...,
		minute: int | EllipsisType = ...,
		second: int | EllipsisType = ...,
		microsecond: int | EllipsisType = ...,
		tz: _TzInfo | None = tz,
		offset: Δ | None = Δ(0),
		__kwargs: dict[str, int] = ...,
	):
		if "tz" in __kwargs:
			del __kwargs["tz"]

		if "offset" in __kwargs:
			del __kwargs["offset"]

		if offset is None:
			offset = Δ(0)

		def mock_datetime_now(tz: _TzInfo = tz, __offset=offset):
			return datetime.now(tz=tz).replace(**__kwargs) + __offset

		return mock_datetime_now, mock_datetime_now()


@pytest.mark.parametrize(
	("m",),
	(
		(1,),
		(2,),
		(3,),
		(7,),
		(10,),
	),
)
def test_robostr_all_units(true_now: datetime, *, m: int):
	mdtn, mock_now = mdtn_factory(**datetime_dict(true_now))

	parse = partial(t.parse, tz=tz, _datetime_now=mdtn)

	if now_1s := mock_now + Δ(seconds=1) * m:
		assert eq_datetime(parse(f"{m}s"), now_1s)
		assert eq_datetime(parse(f"{m}sec"), now_1s)
		assert eq_datetime(parse(f"{m}secs"), now_1s)
		assert eq_datetime(parse(f"{m}sex"), now_1s)
		assert eq_datetime(parse(f"{m}second"), now_1s)
		assert eq_datetime(parse(f"{m}seconds"), now_1s)

	if now_1m := mock_now + Δ(minutes=1) * m:
		assert eq_datetime(parse(f"{m}m"), now_1m)
		assert eq_datetime(parse(f"{m}min"), now_1m)
		assert eq_datetime(parse(f"{m}mins"), now_1m)
		assert eq_datetime(parse(f"{m}minute"), now_1m)
		assert eq_datetime(parse(f"{m}minutes"), now_1m)

	if now_1h := mock_now + Δ(hours=1) * m:
		assert eq_datetime(parse(f"{m}h"), now_1h)
		assert eq_datetime(parse(f"{m}hr"), now_1h)
		assert eq_datetime(parse(f"{m}hrs"), now_1h)
		assert eq_datetime(parse(f"{m}hour"), now_1h)
		assert eq_datetime(parse(f"{m}hours"), now_1h)

	if now_1d := mock_now + Δ(days=1) * m:
		assert eq_datetime(parse(f"{m}d"), now_1d)
		assert eq_datetime(parse(f"{m}day"), now_1d)
		assert eq_datetime(parse(f"{m}days"), now_1d)

	if now_1w := mock_now + Δ(days=7) * m:
		assert eq_datetime(parse(f"{m}w"), now_1w)
		assert eq_datetime(parse(f"{m}week"), now_1w)
		assert eq_datetime(parse(f"{m}weeks"), now_1w)

	if now_1y := mock_now + Δ(days=365) * m:
		assert eq_datetime(parse(f"{m}y"), now_1y)
		assert eq_datetime(parse(f"{m}year"), now_1y)
		assert eq_datetime(parse(f"{m}years"), now_1y)

	if now_1decade := mock_now + Δ(days=365 * 10) * m:
		assert eq_datetime(parse(f"{m}decade"), now_1decade)
		assert eq_datetime(parse(f"{m}decades"), now_1decade)

	if now_1rescue := mock_now + Δ(hours=6) * m:
		assert eq_datetime(parse(f"{m}res"), now_1rescue)
		assert eq_datetime(parse(f"{m}reses"), now_1rescue)
		assert eq_datetime(parse(f"{m}resees"), now_1rescue)
		assert eq_datetime(parse(f"{m}rescue"), now_1rescue)
		assert eq_datetime(parse(f"{m}rescues"), now_1rescue)

	if now_1pull := mock_now + Δ(hours=11, minutes=30) * m:
		assert eq_datetime(parse(f"{m}pul"), now_1pull)
		assert eq_datetime(parse(f"{m}pull"), now_1pull)
		assert eq_datetime(parse(f"{m}puls"), now_1pull)
		assert eq_datetime(parse(f"{m}pulls"), now_1pull)
		assert eq_datetime(parse(f"{m}card"), now_1pull)
		assert eq_datetime(parse(f"{m}cards"), now_1pull)


def test_robostr_multi_subsegment(true_now: datetime):
	mdtn, mock_now = mdtn_factory(**datetime_dict(true_now))

	for s, δ in (
		("1h15m", Δ(hours=1, minutes=15)),
		("2h-4m", Δ(hours=2, minutes=-4)),
		("-.5h", Δ(hours=-0.5)),
	):
		assert eq_datetime(
			t.parse(s, tz=tz, _datetime_now=mdtn),
			mock_now + δ,
		)


@pytest.mark.parametrize(
	("weekday_str", "weekday_num"),
	(
		("mon", 0),
		("tue", 1),
		("wed", 2),
		("thu", 3),
		("fri", 4),
		("sat", 5),
		("sun", 6),
	),
)
def test_weekday_with_mock(true_now: datetime, *, weekday_str: str, weekday_num: int):
	mdtn, mock_now = mdtn_factory(
		hour=true_now.hour,
		minute=0,
		second=1,
		microsecond=0,
		tz=tz,
	)

	calculated = mock_now + Δ(days=1)

	while calculated.weekday() != weekday_num:
		calculated = calculated + Δ(days=1)

	assert eq_datetime(t.parse(weekday_str, tz=tz, _datetime_now=mdtn), calculated)


_test_time_with_mock_parametrize_body = [
	( None, None, None, Δ(0)       ),
	( None, 0,    1,    Δ(0)       ),
	( None, 0,    0,    Δ(0)       ),
	( 13,   None, None, Δ(0)       ),
	( 13,   0,    1,    Δ(0)       ),
	( 13,   0,    0,    Δ(0)       ),
	( 21,   None, None, Δ(0)       ),
	( 21,   0,    1,    Δ(0)       ),
	( 21,   0,    0,    Δ(0)       ),
	( None, None, None, Δ(days=1)  ),
	( None, 0,    1,    Δ(days=1)  ),
	( None, None, None, Δ(days=-1) ),
	( None, 0,    1,    Δ(days=-1) ),
]  # fmt: skip


@pytest.mark.parametrize(("h", "m", "s", "offset"), _test_time_with_mock_parametrize_body)
def test_time_with_mock(true_now: datetime, *, h: int | None, m: int | None, s: int | None, offset: Δ):
	mdtn, mock_now = mdtn_factory(
		hour=h if h is not None else true_now.hour,
		minute=m if m is not None else true_now.minute,
		second=s if s is not None else true_now.second,
		microsecond=0,
		offset=offset,
		tz=tz,
	)

	for st, hh, mm, ss in [
		(f"{mock_now.hour}:", mock_now.hour, 0, 0),
		(f"{mock_now.hour}::", mock_now.hour, 0, 0),
		(f"{mock_now.hour}:6:9", mock_now.hour, 6, 9),
	]:
		assert eq_datetime(
			t.parse(
				st,
				_datetime_now=mdtn,
			),
			mock_now.replace(minute=mm, second=ss) + Δ(days=int(mock_now.timetz() >= time(hour=hh, minute=mm, second=ss, tzinfo=tz))),
		)
