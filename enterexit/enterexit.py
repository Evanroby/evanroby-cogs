from redbot.core import commands, Config
import discord

class EnterExit(commands.Cog):
    """Enter & Exit Announcements Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=987654321)
        self.config.register_guild(required_role=None, enter_emoji="👋", exit_emoji="🚪")

    async def has_required_role(self, ctx):
        """Check if user has the required role"""
        role_id = await self.config.guild(ctx.guild).required_role()
        if role_id is None:
            return True
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        return role in ctx.author.roles if role else False

    async def can_use_emoji(self, ctx, emoji: str):
        """Check if bot can send the given emoji"""
        if emoji.startswith("<") and emoji.endswith(">"):  
            emoji_id = emoji.split(":")[-1][:-1]  
            return discord.utils.get(ctx.guild.emojis, id=int(emoji_id)) is not None
        return True  

    @commands.guild_only()
    @commands.command(name="enter")
    async def enter(self, ctx, user: discord.User):
        """Enter the chat."""
        if not await self.has_required_role(ctx):
            return await ctx.send("❌ **You don't have permission to use this command.**")
        
        enter_emoji = await self.config.guild(ctx.guild).enter_emoji()
        if not await self.can_use_emoji(ctx, enter_emoji):
            enter_emoji = "👋"  
        
        await ctx.send(f"**{user.mention}** **entered the chat** {enter_emoji}")

    @commands.guild_only()
    @commands.command(name="exit")
    async def exit(self, ctx, user: discord.User):
        """Exit the chat."""
        if not await self.has_required_role(ctx):
            return await ctx.send("❌ **You don't have permission to use this command.**")
        
        exit_emoji = await self.config.guild(ctx.guild).exit_emoji()
        if not await self.can_use_emoji(ctx, exit_emoji):
            exit_emoji = "🚪"  
        
        await ctx.send(f"**{user.mention}** **exited the chat** {exit_emoji}")

    async def is_guild_owner(self, ctx):
        """Check if user is the server owner"""
        if ctx.author.id != ctx.guild.owner_id:
            await ctx.send("❌ **You must be the server owner to use this command.**")
            return False
        return True

    @commands.guild_only()
    @commands.command(name="setrequiredrole")
    async def set_required_role(self, ctx, role: discord.Role = None):
        """Set a required role for enter/exit commands (Server Owner Only)."""
        if not await self.is_guild_owner(ctx):
            return
        await self.config.guild(ctx.guild).required_role.set(role.id if role else None)
        if role:
            await ctx.send(f"✅ **Required role set to:** {role.mention}")
        else:
            await ctx.send("✅ **Removed required role. Anyone can use the commands now.**")

    @commands.guild_only()
    @commands.command(name="setenteremoji")
    async def set_enter_emoji(self, ctx, emoji: str):
        """Set a custom emoji for the enter command (Server Owner Only)."""
        if not await self.is_guild_owner(ctx):
            return
        if not await self.can_use_emoji(ctx, emoji):
            return await ctx.send("⚠️ **I can't use that emoji! Make sure I'm in the server where it's from.**")
        await self.config.guild(ctx.guild).enter_emoji.set(emoji)
        await ctx.send(f"✅ **Enter emoji set to:** {emoji}")

    @commands.guild_only()
    @commands.command(name="setexitemoji")
    async def set_exit_emoji(self, ctx, emoji: str):
        """Set a custom emoji for the exit command (Server Owner Only)."""
        if not await self.is_guild_owner(ctx):
            return
        if not await self.can_use_emoji(ctx, emoji):
            return await ctx.send("⚠️ **I can't use that emoji! Make sure I'm in the server where it's from.**")
        await self.config.guild(ctx.guild).exit_emoji.set(emoji)
        await ctx.send(f"✅ **Exit emoji set to:** {emoji}")
      
