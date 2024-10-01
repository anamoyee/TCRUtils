# TCRUtils - Utility Package for TCR Projects

`TCRUtils` is a collection of utility functions, classes, and helpers designed to streamline various tasks in TCR projects. Below is a brief overview of some of the key features.

## Installation and Importing

Importing '''convention''' (it's just me using it...)
```python
import tcrutils as tcr
```

Star-importng is supported (overriden) but you'd be a lot better off by just importng by name or the module itself not to litter your global scope with all this garbage
```python
from tcrutils import timestr
```

## Featured Features (yipee :3)

- **`fmt_iterable(x: LITERALLY_ANY_OBJECT_TYPE)`**: Pretty-formats any python object that i have thought of for easier readability, even some third-party-library ones.
- **`console`, or just `tcr.c`**: Provides [hikari](https://pypi.org/project/hikari/)-styled logging combined with the above fmt_iterable to pretty-print your debugging! Yay!
- **`TStr`**: Convert between seconds and readable timestrs. Now with timezones! for example `str("1h")` -> `int(3600)`.
- **`ShelveDB`**: Quickly and easily set up a dict-based, python built-in shelve module's shelf - a python dictionary able to contain arbitrary python types that persists on restart.

### Iterable Helpers
- **`Or`**: Returns the first element of the tuple (arg, *args) that does not equal the supplied (`none`) variable, by default None. This is different from just doing `x or y or y` because it does not fail on falsey values, just the ones that are specified to be equal to the noney value
- **`batched`**: py3.12 itertools.batched() in py3.11 with some extra features!
- **`cut_at`**: Cut a string (or an iterable) with a specified suffix for example i'm running out of space on this markdown line so i will use th...
- **`shuffled`**: Returns a shuffled version of an iterable. So you dont have to do `random.shuffle(x)` which does not return the shuffled

### String and Formatting Utilities
- **`commafy`**: Adds commas to numbers for better readability.
- **`apostrophe_s`**: Handles the correct placement of apostrophes if the word ends with s for example `"peoples'"` and `"mike's"` (not `"peoples's"`).

### Error Handling
- **`extract_error` and `extract_traceback`**: Extracts the error object's name and the error message (or the traceback's contents).

### Decorators
- **`@autorun`**: Automatically runs the the function whenever its definition is completed.
- **`@timeit`**: Measures the execution time of a function and prints it to the screen.

### Miscellaneous
- **`insist`**: Prompts user input with a customizable insistence until a valid answer is provided, for example you can keep input()ing the user if they provided invalid value for an integer field.

This package includes many other useful utilities, go look for yourself if you want...
