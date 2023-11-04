import typing as t

from colored import attr, bg, fg, stylize

from .tcr_extract_error import extract_error

color_aliases = {
  "gold": 'yellow',
}

class Color:
  RESET:    str        # Reset constant
  _default: str | None # Color that will be applied on invalid color

  def __init__(self) -> None:
    self.RESET    = stylize('', attr(0))
    self._default = None

  def _get_default_color(self, name=''):
    if self._default is None:
      msg = f'Invalid color: \'{name}\''
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

  def __call__(self, color: str, text: str | None = None) -> str:
    """Abstraction for easier ansi coloring & formatting."""

    if not color:
      return self._get_default_color()

    if color.replace('_', '').lower() == 'reset': return self.RESET

    attr_und  = '_' in color; color = color.replace('_', '') # Underlined if it contains _
    attr_dim  = '&' in color; color = color.replace('&', '') # Dim        if it contains &
    attr_bli  = '*' in color; color = color.replace('*', '') # Blink      if it contains *
    attr_rev  = '!' in color; color = color.replace('!', '') # Reverse    if it contains !
    attr_hidd = '#' in color; color = color.replace('#', '') # Hidden     if it contains #

    attr_bold = color[0] == color[0].upper()                # Bold if the first letter is uppercase
    is_bg     = color == color.upper()                      # bg if all caps

    color = color.lower()

    if color in color_aliases:
      color = color_aliases[color]

    styles = []
    try:
      styles.append((bg if is_bg else fg)(color))
    except KeyError:
      return self._get_default_color(color)
    if attr_bold: styles.append( attr( 'bold'       ))
    if attr_und:  styles.append( attr( 'underlined' ))
    if attr_dim:  styles.append( attr( 'dim'        ))
    if attr_bli:  styles.append( attr( 'blink'      ))
    if attr_rev:  styles.append( attr( 'reverse'    ))
    if attr_hidd: styles.append( attr( 'hidden'     ))

    if text is None:
      return stylize('', ''.join(styles), reset=False)
    return styles(text, ''.join(styles))
color = Color()
del Color
c, colour = color, color
