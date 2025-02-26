from redbot.core import commands
import discord
import random
import io

class StealSticker(commands.Cog):
    """Steal a sticker from a message and add it to the guild."""

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        """Called when the cog is loaded."""
        print("StealSticker cog has been loaded.")

    async def cog_unload(self):
        """Called when the cog is unloaded."""
        print("StealSticker cog has been unloaded.")

    @commands.command(name="stealsticker")
    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    async def stealsticker(self, ctx: commands.Context, message_id: int):
        """Steal a sticker from a message and add it to the server."""
        await ctx.send("\U0001F50D Stealing your sticker...")

        try:
            message = await ctx.channel.fetch_message(message_id)
            if not message.stickers:
                return await ctx.send("⚠️ There is no sticker in that message.")

            sticker = message.stickers[0]

            if sticker.url.endswith(".json"):
                return await ctx.send("⚠️ That is not a valid sticker file.")

            sticker_bytes = await sticker.read()
            sticker_file = discord.File(io.BytesIO(sticker_bytes), filename=f"{sticker.name}.png")

            guild_emojis = ctx.guild.emojis
            emoji = str(random.choice(guild_emojis)) if guild_emojis else "🔥"

            try:
                created = await ctx.guild.create_sticker(
                    name=sticker.name,
                    description=getattr(sticker, 'description', ""),
                    file=sticker_file,
                    emoji=emoji  
                )
                await ctx.send(f"✅ Created your sticker using the name **{created.name}** with emoji {emoji}!")
            except discord.HTTPException as err:
                if err.code == 30039:  
                    await ctx.send("⚠️ Your guild has reached the **sticker limit**.")
                else:
                    await ctx.send("⚠️ An unknown error occurred while adding the sticker.")

        except discord.NotFound:
            await ctx.send("⚠️ Could not find the message. Please provide a valid message ID.")
        except discord.Forbidden:
            await ctx.send("⚠️ I don't have permission to manage stickers in this server.")
        except Exception as e:
            await ctx.send(f"⚠️ An unexpected error occurred: {e}")

async def setup(bot):
    await bot.add_cog(StealSticker(bot))
