import typing as t

from colored import attr, bg, fg, stylize

from .tcr_extract_error import extract_error

color_aliases = {
  'gold': 'yellow',
}


class Color:
  RESET: str  # Reset constant
  _default: str | None  # Color that will be applied on invalid color

  def __init__(self) -> None:
    self.RESET = stylize('', attr(0))
    self._default = None

  def _get_default_color(self, name=''):
    if self._default is None:
      msg = f'Invalid color: {name!r}'
      raise ValueError(msg)
    return self._default

  @property
  def default(self):
    return self._default

  @default.setter
  def default(self, color: str | None = None) -> str:
    if color is None:
      self._default = None
      return
    if not isinstance(color, str):
      msg = f'Invalid color type, must be str, got {type(color)}'
      raise TypeError(msg)
    self._default = self(color)

  def __call__(self, *colors: str | None) -> str:
    """Abstraction for easier ansi coloring & formatting."""

    if len(colors) >= 2:
      return ''.join([self.__call__(x) for x in colors])
    else:
      if colors == ():
        return self.RESET
      colors = colors[0]

    if str(colors).lower() in ['reset', '0']:
      return self.RESET

    if isinstance(colors, int):
      return fg(colors)

    colors = colors.replace(
      '\\_', '🚜🚛🚚🚚🚚🚒🚝🚈🚈🚈🚅🚅🚄🚔🚔🚘🚘🚜🚜🚛🚛🚛🚚🚚🚒🚒🚑🚑'
    )  # Underlined if it contains _
    attr_und = '_' in colors
    colors = colors.replace('_', '')  # Underlined if it contains _
    colors = colors.replace(
      '🚜🚛🚚🚚🚚🚒🚝🚈🚈🚈🚅🚅🚄🚔🚔🚘🚘🚜🚜🚛🚛🚛🚚🚚🚒🚒🚑🚑', '_'
    )  # Underlined if it contains _
    attr_dim = '&' in colors
    colors = colors.replace('&', '')  # Dim        if it contains &
    attr_bli = '*' in colors
    colors = colors.replace('*', '')  # Blink      if it contains *
    attr_rev = '!' in colors
    colors = colors.replace('!', '')  # Reverse    if it contains !
    attr_hidd = '#' in colors
    colors = colors.replace('#', '')  # Hidden     if it contains #

    attr_bold = colors[0] == colors[0].upper()  # Bold if the first letter is uppercase
    is_bg = colors == colors.upper() and not colors.isnumeric()  # bg if all caps

    colors = colors.lower()

    if colors in color_aliases:
      colors = color_aliases[colors]

    styles = []
    try:
      styles.append((bg if is_bg else fg)(colors))
    except KeyError:
      return self._get_default_color(colors)
    if attr_bold:
      styles.append(attr('bold'))
    if attr_und:
      styles.append(attr('underlined'))
    if attr_dim:
      styles.append(attr('dim'))
    if attr_bli:
      styles.append(attr('blink'))
    if attr_rev:
      styles.append(attr('reverse'))
    if attr_hidd:
      styles.append(attr('hidden'))

    return stylize('', ''.join(styles), reset=False)

  def __str__(self) -> str:
    return c()


color = Color()
del Color
c, colour = color, color


def printc(*args, end='\n', **kwargs):
  end = c('reset') + end
  return print(*args, end=end, **kwargs)
