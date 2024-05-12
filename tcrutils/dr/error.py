class DynamicResponseError(Exception):
  """Base class for all dynamic responses errors."""


class DynamicResponsePlaceholderMissingContextError(DynamicResponseError, TypeError):
  """A placeholder requires a dependency which is missing."""


class DynamicResponseMissingPlaceholderError(DynamicResponseError, KeyError):
  """Placeholder that was requested doesn't exist.

  (Is not raised if the error_on_missing_placeholder is set to False, in that case the literal text for the placeholder will be returned as the missing placeholder's return value.)

  ```py
  execute = DynamicResponseBuilder(placeholders={
    "test": lambda *args, **kwargs: "TEST",
    "test2": lambda *args, **kwargs: "TEST2",
  })

  execute("{unknown_placeholder}") # Will raise ExecuteMissingPlaceholderError because 'unknown_placeholder' placeholder doesn't exist in the provided set.
  """


class DynamicResponseSyntaxError(DynamicResponseError, ValueError):
  """Syntax error in dynamic response's input text (for example mismatched parenthesis)."""


class DynamicResponseRecursionError(DynamicResponseError, RecursionError):
  """Python's recursion limit was reached when evaluating a dynamic response. (for example placeholder tried to replace itself with itself so it got called again and again and you get the idea...)."""


class DynamicResponsePlaceholderInvalidReturnError(DynamicResponseError, ValueError):
  """Placeholder returned an invalid value and raise_invalid_placeholder_return is set to True."""


class DynamicResponsePythonErrorInPlaceholerError(DynamicResponseError):
  """Is raised when a Python error occurs within placeholder callable."""


class DynamicResponsePlaceholderTooFewArgumentsError(DynamicResponseError, TypeError):
  """Placeholder requires more arguments than were provided.

  Example: {char} # char of.. what? you did not supply the argument.
  Simillar to python's 'TypeError: function() missing X required positional argument(s): ...'
  """


class DynamicResponsePlaceholderTooManyArgumentsError(DynamicResponseError, TypeError):
  """Placeholder requires strictly fewer arguments than were provided.

  This will probably be rarely used since in most cases the better approach is to ignore the extra arguments.

  Example: {char|0x4|0x3|0x2|0x1} # Too many arguments (assuming {char} doesn't support *args).
  Simillar to python's 'TypeError: function() takes X positional argument(s) but Y were given'
  """
