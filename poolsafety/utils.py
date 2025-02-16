async def is_guild_owner_or_assigned(config, guild, user):
    """Checks if the user is the guild owner or an assigned extra owner."""
    guild_settings = await config.guild(guild).all()
    return user.id == guild.owner_id or user.id in guild_settings["owners"]
