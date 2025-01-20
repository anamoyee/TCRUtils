from collections.abc import Callable, Coroutine, Iterable
from functools import partial
from typing import Any

import hikari
import miru
import miru.view

from . import tcrd_types as dtypes
from .tcrd_embeds import embed, modal


class UpdatableView(miru.View):
	async def update(self) -> None:
		await self.message.edit(components=self)


class DisableableView(UpdatableView):
	async def on_timeout(self) -> None:
		await self.disable(edit=True, stop=False)
		return await super().on_timeout()

	async def disable(self, *, edit: bool = True, stop: bool = True) -> None:  # cripple_youth()
		"""Set `disabled` of all children to True. Optionally edit the message with new view and/or stop the view listener for interactions."""
		for ch in self.children:
			ch.disabled = True

		if edit:
			await self.update()

		if stop:
			self.stop()


class CallbackedButton(miru.Button):
	__init_kwargs: dict
	__callback: Callable[["CallbackedButton", miru.ViewContext], Coroutine[Any, Any, None]]

	def __init_subclass__(cls, **kwargs) -> None:
		cls.__init_kwargs = kwargs

	def __init__(self, callback: Callable[["CallbackedButton", miru.ViewContext], Coroutine[Any, Any, None]], /, *, disable_on_click: bool = True, **kwargs) -> None:
		self.__callback = callback
		self.__disable_on_click = disable_on_click
		super().__init__(**{**self.__init_kwargs, **kwargs})

	async def callback(self, ctx: miru.ViewContext) -> None:
		if self.__disable_on_click:
			await ctx.view.disable(edit=True, stop=True)  # type: ignore
		await self.__callback(self, ctx)


class YesButton(CallbackedButton, label="Yes", style=hikari.ButtonStyle.SUCCESS): ...


class NoButton(CallbackedButton, label="No", style=hikari.ButtonStyle.DANGER): ...


class MaybeButton(CallbackedButton, label="Maybe", style=hikari.ButtonStyle.PRIMARY): ...


async def confirm(
	responder: dtypes.HikariResponder,
	miru_client: miru.Client,
	*,
	yes_callback: Callable[[miru.Button, miru.ViewContext], Coroutine[Any, Any, None]],
	no_callback: Callable[[miru.Button, miru.ViewContext], Coroutine[Any, Any, None]],
	buttons: Iterable[miru.Button | bool] = (True, False),
	disable_on_click: bool = True,
	responder_kwargs: dtypes.HikariDictMessage = {"content": "Please choose an option"},  # noqa: B006
	view_kwargs: dict = {"timeout": 2 * 60},  # noqa: B006
) -> hikari.Message:
	"""Send a rather simple confirmator for user to click yes/no."""

	buttons = [YesButton(yes_callback, disable_on_click=disable_on_click) if x is True else x for x in buttons]
	buttons = [NoButton(no_callback, disable_on_click=disable_on_click) if x is False else x for x in buttons]

	view = DisableableView(**view_kwargs)

	for btn in buttons:
		view = view.add_item(btn)  # type: ignore

	m = await responder(components=view, **responder_kwargs)  # type: ignore
	miru_client.start_view(view, bind_to=m)

	return m
