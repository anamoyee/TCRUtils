try:
	from . import placeholder_sets as placeholder_set
	from . import placeholders as placeholder
	from .core import (
		DynamicResponseBuilder,
		DynamicResponseError,
		DynamicResponseMissingPlaceholderError,
		DynamicResponsePlaceholderInvalidReturnError,
		DynamicResponseRecursionError,
		DynamicResponseSyntaxError,
	)
except ImportError:
	...
