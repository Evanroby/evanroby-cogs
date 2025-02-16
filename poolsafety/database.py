from redbot.core import Config

config = Config.get_conf(None, identifier=10115460371, force_registration=True)

default_guild = {
    "whitelist": [],
    "quarantine_role": None,
    "enabled": False,
    "owners": []
}

config.register_guild(**default_guild)
