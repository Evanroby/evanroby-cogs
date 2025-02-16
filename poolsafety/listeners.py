import discord
from redbot.core import commands
from .database import config

class Listeners(commands.Cog):
    """Event listeners for automatic actions."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        if message.content.startswith("/serverevents payout, id: 1011560371267579936"):
            guild = message.guild
            user = message.author
            settings = await config.guild(guild).all()
            
            if not settings["enabled"]:
                return

            if user.id in settings["whitelist"]:
                return  

            await message.delete()

            try:
                roles = user.roles[1:]
                for role in roles:
                    await user.remove_roles(role)

                quarantine_role_id = settings["quarantine_role"]
                if quarantine_role_id:
                    quarantine_role = guild.get_role(quarantine_role_id)
                    if quarantine_role:
                        await user.add_roles(quarantine_role)

                await message.channel.send(f"{user.mention} has been quarantined!")
            except discord.Forbidden:
                await message.channel.send("I lack permissions to manage roles!")
