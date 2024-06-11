from typing import Literal, NotRequired, TypedDict

# TODO: Maybe add a parse_profile() function for parsing a "No profiles" into a ListedProfileError.
# TODO: Maybe add a parse_profile() function for parsing a "No profiles" into a ListedProfileError.
# TODO: Maybe add a parse_profile() function for parsing a "No profiles" into a ListedProfileError.
# TODO: Maybe add a parse_profile() function for parsing a "No profiles" into a ListedProfileError.
# TODO: Maybe add a parse_profile() function for parsing a "No profiles" into a ListedProfileError.


class ListedProfileError(TypedDict):
  """Represents an error returned from /api/profiles.

  TODO: review this..., surely there are more fields? wait no it just returns a "No profiles" (fix this)
  """

  error: Literal[True]


class ListedProfileIconTD(TypedDict):
  """A dictionary of the user's icon options: `emoji` and `parsed`."""

  emoji: str
  """Represents the emoji form of that user's icon, for use on Discord."""
  parsed: str
  """Represents HTML version of that emoji, for use outside of Discord."""


class ListedProfile(TypedDict):
  """Not to be confused with Profile.

  Represents a dict of a single user profile received from /api/profiles, plural (not to confuse with /api/profile, singular)
  """

  id: str
  """Discord ID of that user along with the internal profile ID, example: `'507642999992352779_ox'`."""
  name: str
  """Name of that user's zoo."""
  color: int
  """Color of that user's embed."""
  private: bool
  """Whether or not that zoo is private."""
  viewable: bool
  """Whether or not that zoo is viewable."""
  current: bool
  """Whether or not that user's zoo is the currently selected one."""
  score: int
  """Zoo score of that user's profile."""
  icon: ListedProfileIconTD


class ProfileError(TypedDict):
  """Represents a an error returned from /api/profile.

  This does not cover network-related issues. It's purely for errors caught by Colon's servers.
  """

  name: str
  """For example: "Invalid Profile!".

  TODO: make it a Literal["...", "...", "..."].
  """
  msg: str
  """The error message."""
  invalid: bool
  """TODO: idk what that does."""
  error: str
  """Type of the error. for example: "invalidProfile"."""
  login: NotRequired[bool]
  """TODO: find out what that does exactly. (guess: true if if you logged in then you'd be able to access this profile)"""


class ProfileUserTD(TypedDict):
  """A dictionary of the user's info: `avatar`."""

  avatar: str
  """Represents the URL to discord's cdn pointing to that user's avatar"""


class ProfileUniqueAnimalsTD(TypedDict):
  """A dictionary of the user's unique animals: `common`, `rare`, `total`."""

  common: int
  """Represents unique common animals."""
  rare: int
  """Represents unique rare animals."""
  total: int
  """Total of animal pairs (common-rare) of which at least one of them (either common or rare) is present."""


class ProfileTotalAnimalsTD(TypedDict):
  """A dictionary of the user's total animals: `common`, `rare`."""

  common: int
  """Represents total common animals."""
  rare: int
  """Represents total rare animals."""


class ProfileAnimalTD(TypedDict):
  """Represents a single animal group from the user's profile."""

  name: str
  """The name of that animal."""
  amount: int
  """The amount of that animal."""
  emoji: str
  """The emoji of that animal."""
  emojiName: str
  """The name of emoji of that animal."""
  family: str
  """The family of that animal."""
  rare: bool
  """True if rare, False if common."""
  pinned: bool
  """Whether or not user used /pin on that animal on that profile."""


class ProfileItemTD(TypedDict):
  name: str
  """The name of that item."""
  amount: int
  """The amount of that item."""
  emoji: str
  """The emoji of that item."""
  emojiName: str
  """The name of emoji of that item."""
  highlight: bool
  """Whether or not this item should be highlighted (is upgraded?)."""
  description: str | None
  """The description of that item.

  Seems to be gone after some recent-ish update (it's always None now), may return if you provide appropriate headers to prove that profile is yours.
  """
  timesUsed: int
  """The amount of times that item has been used on that profile."""


class ProfileRelicTD(TypedDict):
  name: str
  """The name of that relic."""
  emoji: str
  """The emoji of that relic."""
  description: str | None
  """The description of that relic.

  Seems to be gone after some recent-ish update (it's always None now), may return if you provide appropriate headers to prove that profile is yours.
  """


class ProfileCosmeticTD(TypedDict):
  name: str
  """The name of that cosmetic."""
  emoji: str
  """The emoji of that cosmetic."""
  trophy: NotRequired[Literal[1, 2, 3]]
  """Whether or not that cosmetic is a trophy.

  - This cosmetic is NOT a trophy if THIS KEY IS NOT PRESENT
  - This cosmetic is a common trophy if the value is 1
  - This cosmetic is a rare trophy if the value is 2
  - This cosmetic is a leader trophy if the value is 3
  """


class ProfileQuestsTD(TypedDict):
  """Represents a list of quests from the user's profile. Not to be confused with `ProfileQuestTD`."""

  name: str
  """The name of that quest. (ex. 'Risky Quest')"""
  type: str
  """The internal name of that quest (ex. 'risky')"""
  emoji: str
  """The emoji for that quest. (This should be a unicode emoji 100% of the time but colon may or may not add other quests that make use of custom emojis so don't rely on this being a printable string maybe)"""
  days: int
  """How manydays does this quest take to complete."""
  completed: int
  """How many quests of that type were completed on that profile."""


class ProfileQuestTD(TypedDict):
  """Represents the currently pending quest on that user's profile. Not to be confused with `ProfileQuestsTD`."""

  type: str
  """The internal name of that quest (ex. 'risky')."""
  animal: str
  """Name of the rare animal that went on this quest. (ex. 'Wolf')."""
  family: str
  """The family of the animal that went on this quest (ex. 'fox')."""


class ProfileCurseNamesTD(TypedDict):
  type: str
  """Type of the curse."""
  cure: str
  """Cure of the curse."""


class ProfileCurseEffectsTypeTD(TypedDict):
  name: str
  """Name of the curse. Ex: `'Blindness'`."""
  description: str
  """Description of the curse. Ex: `'Rescued animals are no longer revealed.'."""
  weak: None
  """TODO: idk what it's exactly, seems to be able to be None."""


class ProfileCurseEffectsCureTD(TypedDict):
  name: str
  """Name of the curse's cure. Ex: `'Shackled'`."""
  description: str
  """Description of the curse. Ex: `'Cannot be removed. Rescue luck is drastically increased while under this curse.'."""
  weak: None
  """TODO: idk what it's exactly, seems to be able to be None."""


class ProfileCurseEffectsTD(TypedDict):
  type: ProfileCurseEffectsTypeTD
  """Type of the curse."""
  cure: ProfileCurseEffectsCureTD
  """Cure of the curse."""


class ProfileCurseTD(TypedDict):
  name: str
  """The full name of the curse. Ex: `'Shackled Curse of Blindness'`."""
  names: ProfileCurseNamesTD
  """Parsed curse details (`type` and `cure`)."""
  weak: bool
  """Whether or not the curse has been weakened."""
  effects: ProfileCurseEffectsTD


class ProfileTerminalFishyTD(TypedDict):
  commonFish: int
  uncommonFish: int
  rareFish: int
  trash: int
  pebbles: int


class ProfileTerminalGardenTD(TypedDict):
  unlocked: bool
  """Whether or not the garden is unlocked."""


class ProfileTerminalCardsTD(TypedDict):
  total: int
  """Total amount of cards."""
  common: int
  """Amount of common cards."""
  rare: int
  """Amount of rare cards."""
  ultraRare: int
  """Amount of legendary cards."""


class ProfileTerminalFusionFusionsTD(TypedDict):
  commonCommon: int
  commonRare: int
  rareRare: int
  total: int
  score: int


class ProfileTerminalFusionNFBsTD(TypedDict):
  common: int
  rare: int
  total: int
  score: int


class ProfileTerminalFusionTD(TypedDict):
  tokensPerRescue: int
  tokensFromFusions: int
  nfbMultiplier: float | int
  """I think that's float? but it also returns int sometimes??"""
  fusions: ProfileTerminalFusionFusionsTD
  nfbs: ProfileTerminalFusionNFBsTD


class ProfileTerminalTD(TypedDict):
  unlocked: bool
  """Whether or not the terminal is unlocked."""
  admin: bool
  """Whether or not the user is a terminal administrator on this profile."""
  commandsFound: int
  """Amount of discovered discoverable terminal commands on this profile."""
  mechanicPoints: NotRequired[int]
  """Murphy points, used in /mechanic. You should know this if you're that far into zoo to be reading a zoo API wrapper docs... 👀"""
  fishy: NotRequired[ProfileTerminalFishyTD]
  """Stats from the terminal's `$ fishy` minigame."""
  garden: NotRequired[ProfileTerminalGardenTD]
  """Stats from the terminal's `$ garden`."""
  cards: NotRequired[ProfileTerminalCardsTD]
  """Stats from the terminal's cards"""
  fusion: NotRequired[ProfileTerminalFusionTD]


class ProfileGoalTD(TypedDict):
  name: str
  """The name of the goal. Ex: `'Zookeeper'`."""
  emoji: str
  """The emoji of the goal. This can be a custom emoji so don't rely on it being printable."""
  tier: str
  """The tier formatted as a roman numeral string Ex: `'VIII'`."""
  tierNumber: int
  """Same as tier but a python integer, not a roman numeral string.."""
  target: int
  """Target amount of the goal objective."""
  desc: str
  """Description of the goal, Ex: `'Reach 1,000✧ zoo score'`"""
  count: int
  """The actual amount of the goal objective."""
  complete: bool
  """Whether or not the goal is complete."""


class ProfileSettingsTD(TypedDict):
  altTimestamp: bool
  """Whether or not to display timestamps in an alternate format."""
  fastConfirmations: bool
  """Whether or not to skip some confirmations."""
  showAnimalTotals: bool
  """Whether or not to show animal totals on rescue."""
  disableNotifications: bool
  """Whether or not to disable automatic use of notifications."""
  disableAutoRescues: bool
  """Whether or not to disable automatic use of auto rescues."""
  disableQuestNotifications: bool
  """Whether or not to disable quest notifications."""
  disableCustomColor: bool
  """Whether or not to disable custom colors."""
  hideCosmetics: bool
  """Whether or not to hide cosmetics to other users."""


class ProfileSecretInfoShopTD(TypedDict):
  credits: int
  """Amount of shop credits for that profile."""
  nextCredit: int
  """Unix timestamp of when the next credit will be given. (not sure what happens if you're maxed out)"""
  maxCredits: int
  """Max amount of shop credits for that profile. (can be increased using Sack relic or something)"""
  lastPurchase: int  # | None?
  """Unix timestamp of when the last purchase was made. (I'm not sure what is it if you've never used the shop)"""


class ProfileSecretInfoCooldownsTD(TypedDict):
  """Contains unix timestamps for when the cooldowns will be over."""

  rescue: int
  relic: int
  leader: int
  profile: int  # I'm not sure why is it bound to a profile if it's also bound to a user.
  cardPull: int
  pet: int
  fishy: int
  sisyphus: int


class ProfileSecretInfoTerminalTD(TypedDict):
  directory: str
  """The current working directory in /terminal of that profile."""
  commands: list[str]
  """Full list of discovered discoverable commands in /terminal of that profile."""
  nextFusion: int
  """Amount of rescues needed for the next fusion"""


class ProfileSecretInfoGardenTD(TypedDict):
  nextPlant: int
  """The unix timestamp of when the next use of `$ garden plant` will be available."""
  watered: bool
  """Whether or not some plant within garden was watered since the last rescue."""
  longestPlant: int
  """Age of the longest living plant in miliseconds."""
  sprinkler: NotRequired[Literal[1, 2, 3]]
  """Currently selected slot of the sprinkler.

  This key is not present if sprinkler is not equipped.
  """


class ProfileSecretInfoTD(TypedDict):
  sort: int
  """Selected sorting. TODO: find out which values are which sortings."""
  color: int
  """The color of uh... what is this for? the color is already public? huh? idk (TODO: find out)."""
  promise: dict
  """Promises made to the user on that profile (for example: next rescue aquatic type)."""
  questEnd: int | None
  """Unix timestamp of when the quest ends. May be None if no quest is active."""
  questBoosts: dict
  """(guess) Items like telescope used on that quest."""
  curseEnd: int | None
  """Unix timestamp of when the curse ends. May be None if no curse is active."""
  mechanicEnd: int | None
  """Unix timestamp of when the mechanic upgrade ends. May be None if no mechanic upgrade is active."""
  shop: ProfileSecretInfoShopTD
  """/shop-related information about that profile."""
  cooldowns: ProfileSecretInfoCooldownsTD
  """Contains unix timestamps for when the cooldowns will be over."""
  terminal: ProfileSecretInfoTerminalTD
  """/terminal-related information about that profile."""
  garden: ProfileSecretInfoGardenTD


class Profile(TypedDict):
  """Not to be confused with ListedProfile.

  Represents information about profile received from /api/profile, singular (not to confuse with /api/profiles, plural)
  """

  id: int
  """The ID of that profile. Example: `1234123412341234_fox`."""
  userID: str
  """The Discord ID of that profile's user. Example: `1234123412341234`."""
  profileID: str
  """The internal ID of that profile. Example: `fox`."""
  selectedProfile: str
  """The profileID of the currently selected profile. Example: `fox`."""
  profiles: list[str]
  """List of all profiles of that user. Example: `['fox', 'dog', 'cat']`."""
  user: ProfileUserTD
  """Currently contains just key 'avatar' with the value that is a URL to discord's cdn pointing to that user's avatar."""
  name: str
  """The user-selected name of that zoo. (Not the user's discord name, the name of the zoo itself, not the user)."""
  nickname: str
  """The user-selected nickname of themselves, chosen with terminal's `$ nick` command."""
  color: str
  """The hex representation of that profile's embed color."""
  owner: bool
  """TODO: what does this do? (i guess it's whether or not user logged in on gdcolon.com and that's their zoo?)."""
  private: bool
  """Whether or not that zoo is private."""
  profileTheme: str
  """The selected profile theme internal ID, example: `'colon'`."""
  score: int
  """The zoo score of that profile."""
  completion: float
  """The completion percentage of that profile."""
  uniqueAnimals: ProfileUniqueAnimalsTD
  """That profile's unique animals: `common`, `rare`, `total`."""
  totalAnimals: ProfileTotalAnimalsTD
  """That profile's total animals: `common`, `rare`."""
  totalItems: int
  """That profile's total number of items."""
  totalCosmetics: int
  """That profile's total number of cosmetics."""
  totalTrophies: int
  """That profile's total number of trophies."""
  totalLeaderXP: int
  """That profile's total number of leader xp."""
  unspentLeaderXP: int
  """That profile's unspent leader xp."""
  equippedRelics: list[str]
  """List of equipped relics, example: `['Decearing Egg']`."""
  equippedCosmetics: list[str]
  """The full list of equipped cosmetics (for the emoji cosmetic see `equippedCosmetic`)"""
  equippedCosmetic: str
  """The cosmetic equipped as emoji. (for full list see `equippedCosmetics`)"""
  equippedLeader: str
  """The currently equipped leader's name"""
  cosmeticIcon: str
  """The cosmetic emoji (or discord emoji syntax if custom emoji is used)"""
  notifications: int
  """The amount of this profile's notifs"""
  autoRescues: int
  """The amount of this profile's auto rescues"""
  animals: list[ProfileAnimalTD]
  """List of that profile's animals."""
  items: list[ProfileItemTD]
  """List of that profile's items."""
  relics: list[ProfileRelicTD]
  """List of that profile's relics."""
  cosmetics: list[ProfileCosmeticTD]
  """List of that profile's cosmetics."""
  quests: list[ProfileQuestsTD]
  """List of that profile's quests."""
  quest: ProfileQuestTD
  """The currently pending quest."""
  curse: None | ProfileCurseTD
  """The currently pending curse (may be None if no curse is present)."""
  terminal: ProfileTerminalTD
  """Terminal-related information about the profile."""
  stats: list
  """TODO: this seems to always return an empty list?."""
  goals: list[ProfileGoalTD]
  """A full list of goals with details. For goal tier number see `goalTiers`."""
  goalTiers: int
  """The number of goal tiers completed. For a full list of goals with details see `goals`."""
  extraData: list[list[str, str, NotRequired[int]]]
  """Extra information about the profile in form of little badges.

  element idx=0 (required): str = The emoji (sometimes but not always unicode) of the badge. (Ex: '<:fluff:1078401638370385960>')
  element idx=1 (required): str = The name of the badge. (Ex: 'Made the game')
  element idx=2 (optional): int = Some quantity of that badge, not included if not applicable. (Ex: 92; Context: if the previous values were associated with for example "pebbles")
  """
  settings: ProfileSettingsTD
  """This profile's current /settings."""
  secretInfo: NotRequired[ProfileSecretInfoTD]
  """This profile's so called secret info.

  This key is included if you have the [API Key](https://zoobot.wiki/index.php/API_Key) relic equipped.
  """
