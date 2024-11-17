from redbot.core import commands
import discord
import asyncio

class CategoryCleaner(commands.Cog):
    """A cog to delete all channels within a specified category."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def delete_category_channels(self, ctx, category_id: int):
        """Deletes all channels within the specified category ID. (Admin Only)"""
        category = discord.utils.get(ctx.guild.categories, id=category_id)
        
        if category is None:
            await ctx.send("Category not found. Please check the ID and try again.")
            return

        confirm_msg = await ctx.send(f"Are you sure you want to delete all channels in the category '{category.name}'? (yes/no)")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["yes", "no"]

        try:
            response = await self.bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out. Please try the command again.")
            return

        if response.content.lower() != "yes":
            await ctx.send("Operation cancelled.")
            return

        deleted_channels = []
        for channel in category.channels:
            await channel.delete()
            deleted_channels.append(channel.name)

        await ctx.send(f"Deleted channels: {', '.join(deleted_channels)}")
