from .enterexit import EnterExit

async def setup(bot):
    bot.add_cog(EnterExit(bot))
