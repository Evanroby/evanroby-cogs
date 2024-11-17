from redbot.core.bot import Red

from .category_cleaner import CategoryCleaner

async def setup(bot: Red):
    await bot.add_cog(CategoryCleaner(bot))
