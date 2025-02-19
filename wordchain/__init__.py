from redbot.core.bot import Red
from .wordchain import WordChain

async def setup(bot: Red):
    cog = WordChain(bot)
    await bot.add_cog(cog)
