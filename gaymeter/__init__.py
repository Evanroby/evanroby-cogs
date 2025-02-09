from .gaymeter import GayMeter

async def setup(bot):
    await bot.add_cog(GayMeter())
