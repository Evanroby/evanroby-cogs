from .simonsays import SimonSays

async def setup(bot):
    await bot.add_cog(SimonSays(bot))
