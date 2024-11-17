from redbot.core.bot import Red
from .core import MoveChannel

async def setup(bot: Red) -> None:
    cog = MoveChannel(bot)
    await bot.add_cog(cog)
