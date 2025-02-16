from redbot.core.bot import Red
from .poolsafety import PoolSafety

async def setup(bot: Red):
    bot.add_cog(PoolSafety(bot))
