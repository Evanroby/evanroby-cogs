import discord
import random
from redbot.core import commands


class GayMeter(commands.Cog):
    """Measures how gay you are!"""

    @commands.command(aliases=["howgay"])
    async def gaymeter(self, ctx, user: discord.Member = None):
        """Measures a user's gayness level.
        
        If no user is mentioned, it defaults to the command author."""
        
        user = user or ctx.author  # Default to author if no user is mentioned
        random.seed(str(user.id))  # Ensures consistent results per user
        gay_percentage = random.randint(0, 100)

        # Custom messages based on percentage
        if gay_percentage < 25:
            message = "You're about as straight as a ruler! 📏"
        elif gay_percentage < 50:
            message = "You're a little curious... 🤔"
        elif gay_percentage < 75:
            message = "You're swinging both ways! 🌈"
        elif gay_percentage < 90:
            message = "You're fabulously gay! 💅🌈"
        else:
            message = "You radiate pure rainbow energy! 🌈✨"

        await ctx.send(f"**{user.display_name} is {gay_percentage}% gay!**\n{message}")
