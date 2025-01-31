import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any


def force_keyword_only_typehints(key: Callable[[Any, type], bool] = isinstance):
	def decorator(func):
		signature = inspect.signature(func)
		kwarg_hints = {name: param.annotation for name, param in signature.parameters.items() if param.kind == param.KEYWORD_ONLY and param.annotation != inspect.Parameter.empty and param.annotation != Any}

		if not kwarg_hints:
			return func

		def validate(arguments):
			for arg_name, arg_type in kwarg_hints.items():
				if arg_name in arguments:
					try:
						validation_result = key(arguments[arg_name], arg_type)
					except Exception as e:
						raise TypeError(f"Unable to validate the input as valid, an error was raised out of the validator:\n  {e.__class__.__name__}: {e}") from e

					if not validation_result:
						raise TypeError(f"Argument '{arg_name}' of {func.__name__}() must be of type {arg_type.__name__}, but got {type(arguments[arg_name]).__name__}.")

		if inspect.iscoroutinefunction(func):

			@wraps(func)
			async def wrapper(*args, **kwargs):
				validate(kwargs)
				return await func(*args, **kwargs)

		else:

			@wraps(func)
			def wrapper(*args, **kwargs):
				validate(kwargs)
				return func(*args, **kwargs)

		return wrapper

	return decorator
