import discord
from redbot.core import commands, checks
from .database import config
from .utils import is_guild_owner_or_assigned

class PoolSafety(commands.Cog):
    """A cog that removes roles when a specific command is run by a non-whitelisted user."""

    def __init__(self, bot):
        self.bot = bot

    async def ensure_guild_owner_whitelisted(self, guild):
        """Ensures that the guild owner is always whitelisted."""
        async with config.guild(guild).whitelist() as whitelist:
            if guild.owner_id not in whitelist:
                whitelist.append(guild.owner_id)

    @commands.group(name="poolsafety", aliases=["ps"])
    @commands.guild_only()
    async def poolsafety(self, ctx):
        """Pool safety settings."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @poolsafety.command(name="showsettings")
    async def showsettings(self, ctx):
        """Shows the current settings for PoolSafety."""
        settings = await config.guild(ctx.guild).all()
        whitelist = settings["whitelist"]
        quarantine_role = settings["quarantine_role"]
        enabled = settings["enabled"]
        extra_owners = settings["owners"]

        role = ctx.guild.get_role(quarantine_role) if quarantine_role else "Not Set"
        users = [ctx.guild.get_member(uid) for uid in whitelist]
        usernames = [u.display_name for u in users if u]

        owners = [ctx.guild.get_member(uid) for uid in extra_owners]
        owner_names = [o.display_name for o in owners if o]

        msg = (
            f"**PoolSafety Settings:**\n"
            f"🔹 **Enabled:** {enabled}\n"
            f"🔹 **Whitelisted Users:** {', '.join(usernames) if usernames else 'None'}\n"
            f"🔹 **Quarantine Role:** {role}\n"
            f"🔹 **Extra Owners:** {', '.join(owner_names) if owner_names else 'None'}\n"
        )
        await ctx.send(msg)

    @poolsafety.command(name="toggle")
    async def toggle(self, ctx):
        """Enables or disables the cog for this server."""
        if not await is_guild_owner_or_assigned(config, ctx.guild, ctx.author):
            return await ctx.send("Only the server owner or assigned owners can manage settings.")

        enabled = await config.guild(ctx.guild).enabled()
        await config.guild(ctx.guild).enabled.set(not enabled)
        status = "enabled" if not enabled else "disabled"
        await ctx.send(f"PoolSafety has been {status}!")

    @poolsafety.command(name="addowner")
    @checks.is_owner()
    async def addowner(self, ctx, user_id: int, guild_id: int):
        """[BOT OWNER ONLY] Adds a user as an extra owner for a specific server."""
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.send("Invalid guild ID.")

        async with config.guild(guild).owners() as owners:
            if user_id not in owners:
                owners.append(user_id)
                await ctx.send(f"User {user_id} has been added as a PoolSafety owner in {guild.name}.")
            else:
                await ctx.send(f"User {user_id} is already an owner in {guild.name}.")

    @poolsafety.command(name="removeowner")
    @checks.is_owner()
    async def removeowner(self, ctx, user_id: int, guild_id: int):
        """[BOT OWNER ONLY] Removes a user's PoolSafety owner status."""
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.send("Invalid guild ID.")

        async with config.guild(guild).owners() as owners:
            if user_id in owners:
                owners.remove(user_id)
                await ctx.send(f"User {user_id} has been removed as a PoolSafety owner in {guild.name}.")
            else:
                await ctx.send(f"User {user_id} is not an owner in {guild.name}.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Ensures the guild owner is whitelisted when the bot joins."""
        await self.ensure_guild_owner_whitelisted(guild)
