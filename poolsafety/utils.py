async def is_guild_owner_or_assigned(config, guild, user):
    """
    Checks if the user is either:
    - The guild owner
    - An assigned extra owner for the guild
    
    Args:
        config: The configuration object storing guild settings.
        guild: The Discord guild (server) object.
        user: The Discord user object.

    Returns:
        bool: True if the user is the owner or an assigned extra owner, otherwise False.
    """
    guild_settings = await config.guild(guild).all()
    return user.id == guild.owner_id or user.id in guild_settings.get("owners", [])


async def ensure_guild_owner_whitelisted(config, guild):
    """
    Ensures that the guild owner is always whitelisted.
    
    Args:
        config: The configuration object storing guild settings.
        guild: The Discord guild (server) object.
    """
    async with config.guild(guild).whitelist() as whitelist:
        if guild.owner_id not in whitelist:
            whitelist.append(guild.owner_id)
