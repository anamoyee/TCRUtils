async def get_guild_count(bot):
  return len(await bot.rest.fetch_my_guilds())
