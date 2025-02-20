from redbot.core.commands import Converter, BadArgument

class RoundsConverter(Converter):
    """Converts input into a valid round number."""
    async def convert(self, ctx, argument):
        try:
            rounds = int(argument)
            if rounds < 1:
                raise BadArgument("Rounds must be a positive number.")
            return rounds
        except ValueError:
            raise BadArgument("Please enter a valid number for rounds.")

class BoolConverter(Converter):
    """Converts various true/false inputs into a boolean."""
    async def convert(self, ctx, argument):
        truthy = ["yes", "true", "1", "on", "enable"]
        falsy = ["no", "false", "0", "off", "disable"]
        arg_lower = argument.lower()

        if arg_lower in truthy:
            return True
        elif arg_lower in falsy:
            return False
        else:
            raise BadArgument("Please use `true/false`, `yes/no`, or `1/0`.")
