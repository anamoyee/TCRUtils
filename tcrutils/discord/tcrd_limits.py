class DiscordLimits:
  class Message:
    LENGTH = 4000
    LENGTH_SAFE = 1984  # Slightly less than 2000 for safety & to fit in a reference hehe
    LENGTH_SAFEST = 1800
    FILE_SIZE_MB = 25

  class Embed:
    TITLE = 256
    DESCRIPTION = 4096
    DESCRIPTION_SAFE = 4000
    AUTHOR_NAME = 256

    class Fields:
      AMOUNT = 25
      TITLE = 256
      DESCRIPTION = 1024

    FOOTER = 2048
    TOTAL_CHARACTERS = 6000
