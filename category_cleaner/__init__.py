from redbot.core.bot import Red

from .core import FirstMessage


async def setup(bot: Red) -> None:
    cog = FirstMessage(bot)
    await bot.add_cog(cog)
