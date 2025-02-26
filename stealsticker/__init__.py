from .stealsticker import StealSticker

async def setup(bot):
    await bot.add_cog(StealSticker(bot))
