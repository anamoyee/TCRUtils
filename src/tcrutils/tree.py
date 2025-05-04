from collections.abc import Callable
from typing import Self

import pydantic as pd

from .console import c
from .print import FMT_ASTERISK, FMT_BRACKETS


class Tree(pd.BaseModel):
	model_config = pd.ConfigDict(
		arbitrary_types_allowed=True,
		validate_assignment=True,
	)

	children: list = pd.Field(default_factory=list)
	_parent: "Self | None" = None

	@property
	def parent(self) -> "Self | None":
		return self._parent

	def __init__(self, **kwargs):
		if "children" in kwargs:
			for child in kwargs["children"]:
				child._parent = self

		super().__init__(**kwargs)

	def __tcr_fmt__(self=None, *, fmt_iterable: Callable[[object], str], syntax_highlighting: bool, **kwargs):
		if self is None:
			raise NotImplementedError

		attrs = self.model_dump()
		del attrs["children"]
		body = FMT_ASTERISK[syntax_highlighting] * 2 + fmt_iterable(attrs, no_implicit_quoteless=True)

		return fmt_iterable(self.__class__) + FMT_BRACKETS[tuple][syntax_highlighting] % body + (fmt_iterable(self.children) if self.children else "")
