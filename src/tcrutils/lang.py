"""Not to be confused with `tcrutils.language`. This module is for language translation helper(s)."""

from collections.abc import Callable, Hashable
from typing import overload

from .print import tcrfmt_dataclass_by_name_args_kwargs as _tcrfmt_dataclass_by_name_args_kwargs


# py313: class Lang[LocaleK: Hashable = str, TranslationK: Hashable = str, V = str]:
class Lang[LocaleK: Hashable, TranslationK: Hashable, V]:
	_d: dict[LocaleK | None, dict[TranslationK, V]]
	_merge_func: Callable[[V, V], V]

	def __init__(self, merge_func: Callable[[V, V], V] = lambda v1, v2: v2):  # converter: Callable[[LocaleK, TranslationK, V], V] = lambda v: v
		self._d = {}
		self._merge_func = merge_func

	def __repr__(self):
		return f"{self.__class__.__name__}({self._d!r})"

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		return _tcrfmt_dataclass_by_name_args_kwargs(
			fmt_iterable=fmt_iterable,
			name=self.__class__.__name__,
			syntax_highlighting=syntax_highlighting,
			obj_kwargs=self._d,
		)

	def _merge_dicts(self, old: dict[TranslationK, V], new: dict[TranslationK, V]) -> dict[TranslationK, V]:
		merged = {}

		all_keys = set(old) | set(new)

		for k in all_keys:
			if k in old and k in new:
				merged[k] = self._merge_func(old[k], new[k])
			elif k in old:
				merged[k] = old[k]
			else:
				merged[k] = new[k]

		return merged

	def merge_localepack(self, locale: LocaleK | None, pack: dict[TranslationK, V]) -> None:
		if locale is not None:
			self._d[None] = pack | self._d.get(None, {})

		self._d[locale] = self._merge_dicts(self._d.get(locale, {}), pack)

	def getitem_localepack(self, locale: LocaleK | None) -> dict[TranslationK, V]:
		return self._d[locale]

	def get_localepack(self, locale: LocaleK | None, default: dict[TranslationK, V] | None = None) -> dict[TranslationK, V] | None:
		return self._d.get(locale, default)

	@overload
	def __getitem__(self, key: LocaleK | None) -> dict[TranslationK, V]: ...

	@overload
	def __getitem__(self, key: tuple[LocaleK | None, TranslationK]) -> V: ...

	@overload
	def __getitem__(self, key: tuple[slice, TranslationK]) -> dict[LocaleK, V]: ...

	def __getitem__(self, key: LocaleK | None) -> dict[TranslationK, V]:
		if not isinstance(key, tuple):
			return self._d[key]

		if not len(key) == 2:
			raise TypeError("if tuple, key must be of length 2")

		k1, k2 = key

		if isinstance(k1, slice):
			if (k1.start, k1.stop, k1.step) != (None, None, None):
				raise ValueError('No compound slices supported, only ":"')

			return {locale: self._d[locale][k2] for locale in self._d if locale is not None if k2 in self._d[locale]}

		return self._d[k1][k2]

	def get_hikari(self, key: TranslationK, *, name: str | None = None) -> dict[str, V | dict[LocaleK, V]]:
		"""Handle hikari (arc) localizations for the given key, return splattable (`**result`) dict with keys: `{name}` and `{name}_localizations` with the appropriate values.

		Args:
			name: If not specified (None), the str(key) will be split by "." and the last part will be used. Warning: this may lead to unexpected results, if the key is not a str itself or does not have a well-made __str__
		"""
		if name is None:
			name = str(key).split(".")[-1]

		localized = self[:, key]

		unlocalized = self[None, key]

		return {
			f"{name}": unlocalized,
			f"{name}_localizations": localized,
		}

	def get_arc_command(self, key: TranslationK) -> dict[str, V | dict[LocaleK, V]]:
		"""Handle hikari-arc's `@slash_command` localizations, by providing a dict with appripriate keys to splat (**result).

		## `!!!` This will only work if the TranslationK generic is str, since it then fetches a value with concatenated str as a key
		"""
		return self.get_hikari(f"{key!s}.name") | self.get_hikari(f"{key!s}.description")


if __name__ == "__main__":

	def __main():
		from hikari import Locale as L

		from .console import c

		LOCALE_INDEP = {
			"hi.name": "hi default name",
			"hi.desc": "hi default desc",
			"bye": "bye default",
		}

		PL = {
			"hi.name": "Witaj",
			"hi.desc": "hej słodziaku~",
			"bye": "Do widzenia",
		}

		EN_GB = {
			"hi.name": "Greetings",
			"hi.desc": "Hi cutie~",
			"hi.extra": "UwU",
			"bye": "Farewell",
		}

		lang = Lang[L]()

		lang.merge_localepack(None, LOCALE_INDEP)

		lang.merge_localepack(L.PL, PL)
		lang.merge_localepack(L.EN_GB, EN_GB)
		lang.merge_localepack(L.EN_GB, {"nya": "nyaa"})

		c(lang[:, "hi.extra"])
		c(lang)
		c("lang[:, 'hi.name']=", eval=True)
		c("lang[:, 'hi.desc']=", eval=True)
		c("lang[L.PL, 'hi.desc']=", eval=True)
		c('lang.get_hikari("hi.name", name="name")=', eval=True)
		c('lang.get_hikari("hi.name")=', eval=True)

		c.hr()

		LOCALE_INDEP2 = {
			"hello": ("Hi", "hai~", "Hello"),
			"bye": ("Bye", "Goodbye"),
		}

		PL2 = {
			"hello": ("Witaj", "hej"),
			"bye": ("Do widzenia", "Do widzenya~"),
		}

		EN_GB2 = {
			"hello": ("Hi", "Hello"),
			"bye": ("Bye", "Goodbye"),
		}

		pools = Lang[L, str, tuple[str]](merge_func=lambda v1, v2: (*v1, *v2))

		pools.merge_localepack(None, LOCALE_INDEP2)

		pools.merge_localepack(L.PL, PL2)
		pools.merge_localepack(L.EN_GB, EN_GB2)
		pools.merge_localepack(L.EN_GB, {"hello": ("hewwo",)})

		c(pools)
		c("pools[:, 'hello']=", eval=True)
		c("pools[:, 'bye']=", eval=True)
		c("pools[L.PL, 'bye']=", eval=True)
		c("pools.get_hikari('hello', name='hello')=", eval=True)

	__main()
