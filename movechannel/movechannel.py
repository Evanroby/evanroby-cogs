from redbot.core import commands, Config
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n
import discord
import typing

_: Translator = Translator("MoveChannel", __file__)

@cog_i18n(_)
class MoveChannel(commands.Cog):
    """Manage and move channels across categories."""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=6452384762, force_registration=True)
        self.config.register_guild()

    async def get_category(self, guild: discord.Guild, category_name_or_id: typing.Union[str, int]) -> typing.Optional[discord.CategoryChannel]:
        if isinstance(category_name_or_id, int):
            return discord.utils.get(guild.categories, id=category_name_or_id)
        return discord.utils.get(guild.categories, name=category_name_or_id)

    async def move_channels_to_category(
        self,
        channels: typing.List[discord.TextChannel],
        category: discord.CategoryChannel,
        reason: str = None
    ) -> None:
        for channel in channels:
            await channel.edit(category=category, reason=reason)

    @commands.guild_only()
    @commands.guildowner()
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.hybrid_group()
    async def movechannel(self, ctx: commands.Context):
        pass

    @movechannel.command(name="move")
    async def move(
        self,
        ctx: commands.Context,
        category_from: typing.Union[discord.CategoryChannel, str],
        category_to: typing.Union[discord.CategoryChannel, str]
    ) -> None:
        guild = ctx.guild

        category_from_obj = await self.get_category(guild, category_from)
        category_to_obj = await self.get_category(guild, category_to)

        if not category_from_obj:
            await ctx.send(_("Category `{}` not found.").format(category_from))
            return
        if not category_to_obj:
            await ctx.send(_("Category `{}` not found.").format(category_to))
            return

        channels = category_from_obj.channels
        if not channels:
            await ctx.send(_("No channels found in category `{}`.").format(category_from_obj.name))
            return

        await self.move_channels_to_category(channels, category_to_obj)
        await ctx.send(
            _("Moved {} channels from `{}` to `{}`.")
            .format(len(channels), category_from_obj.name, category_to_obj.name)
        )

    @movechannel.command(name="list")
    async def list_channels(
        self,
        ctx: commands.Context,
        category: typing.Union[discord.CategoryChannel, str]
    ) -> None:
        guild = ctx.guild
        category_obj = await self.get_category(guild, category)

        if not category_obj:
            await ctx.send(_("Category `{}` not found.").format(category))
            return

        channels = category_obj.channels
        if not channels:
            await ctx.send(_("No channels found in category `{}`.").format(category_obj.name))
        else:
            channel_list = "\n".join([f"- {channel.name}" for channel in channels])
            await ctx.send(
                _("Channels in category `{}`:\n{}").format(category_obj.name, channel_list)
            )

    @commands.slash_command(name="movechannel")
    async def slash_movechannel(
        self,
        ctx: discord.ApplicationContext,
        category_from: discord.Option(str, "Category to move from", autocomplete=True),
        category_to: discord.Option(str, "Category to move to", autocomplete=True)
    ):
        guild = ctx.guild

        category_from_obj = await self.get_category(guild, category_from)
        category_to_obj = await self.get_category(guild, category_to)

        if not category_from_obj:
            await ctx.respond(_("Category `{}` not found.").format(category_from), ephemeral=True)
            return
        if not category_to_obj:
            await ctx.respond(_("Category `{}` not found.").format(category_to), ephemeral=True)
            return

        channels = category_from_obj.channels
        if not channels:
            await ctx.respond(_("No channels found in category `{}`.").format(category_from_obj.name), ephemeral=True)
            return

        await self.move_channels_to_category(channels, category_to_obj)
        await ctx.respond(
            _("Moved {} channels from `{}` to `{}`.").format(len(channels), category_from_obj.name, category_to_obj.name)
        )

    @slash_movechannel.on_autocomplete("category_from")
    @slash_movechannel.on_autocomplete("category_to")
    async def autocomplete_category(
        self, ctx: discord.AutocompleteContext
    ) -> typing.List[str]:
        """Autocomplete for category names."""
        categories = [category.name for category in ctx.guild.categories]
        return [name for name in categories if ctx.value.lower() in name.lower()]

async def setup(bot: Red):
    bot.add_cog(MoveChannel(bot))
