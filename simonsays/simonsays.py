import discord
import random
from redbot.core import commands
from redbot.core.bot import Red
from .converters import RoundsConverter, BoolConverter
from .utils import get_random_command, format_leaderboard, check_response
from typing import Dict, List

class JoinButton(discord.ui.View):
    """View with a button to join the Simon Says game."""
    
    def __init__(self, cog, ctx):
        super().__init__(timeout=10)
        self.cog = cog
        self.ctx = ctx
        self.players = []

    @discord.ui.button(label="Join Game", style=discord.ButtonStyle.green)
    async def join_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handles the player clicking the join button."""
        user = interaction.user
        if user in self.players:
            await interaction.response.send_message("You're already in the game!", ephemeral=True)
            return

        self.players.append(user)
        await interaction.response.send_message("✅ You have joined the game! Check your DMs for instructions. 📩", ephemeral=True)
        
        try:
            dm_embed = discord.Embed(
                title="🎤 Simon Says - How to Play",
                description="Here are the rules so you're ready to play:",
                color=discord.Color.blue()
            )
            dm_embed.add_field(name="📌 Basic Rules", value="Only follow commands that start with **'Simon says'**.\nIf Simon **doesn't** say it, **DO NOT** follow the action!", inline=False)
            dm_embed.add_field(name="🔥 Elimination Mode", value="If enabled, you're **out** if you make a mistake!", inline=False)
            dm_embed.add_field(name="🏆 Winning", value="Players score points for following correct commands. The **highest scorer wins**!", inline=False)
            dm_embed.add_field(name="🎮 Game Flow", value="1. The game starts and players follow instructions.\n2. Each round, Simon will give a command.\n3. Type the exact action if **'Simon says'** is included.\n4. The player with the highest score at the end wins!", inline=False)
            dm_embed.set_footer(text="The game will start soon...")

            await user.send(embed=dm_embed)
        except discord.Forbidden:
            pass  

class SimonSays(commands.Cog):
    """A fun Simon Says game with scoring, rounds, and elimination mode!"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.active_games = {}

    async def cog_load(self):
        """Syncs slash commands when the cog loads."""
        await self.bot.tree.sync()

    @commands.hybrid_command(name="simonsays", with_app_command=True)
    async def simonsays(self, ctx: commands.Context, rounds: RoundsConverter = 5, elimination: BoolConverter = False):
        """
        Start a Simon Says game!
        - `rounds`: Number of rounds (default: 5)
        - `elimination`: Set to True for elimination mode
        """
        if ctx.channel.id in self.active_games:
            await ctx.send("A Simon Says game is already running in this channel!")
            return

        embed = discord.Embed(
            title="🎤 Simon Says - Game Instructions",
            description="Follow Simon's commands correctly to win! Click **Join Game** below to enter.",
            color=discord.Color.blue()
        )
        embed.add_field(name="📌 Basic Rules", value="Only follow commands that start with **'Simon says'**.\nIf Simon **doesn't** say it, **DO NOT** follow the action!", inline=False)
        embed.add_field(name="🔥 Elimination Mode", value="If enabled, you're **out** if you make a mistake!", inline=False)
        embed.add_field(name="🏆 Winning", value="Players score points for following correct commands.\nThe **highest scorer wins**!", inline=False)
        embed.set_footer(text="Click the button below to join!")

        view = JoinButton(self, ctx)
        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if len(view.players) < 2:
            await ctx.send("Not enough players joined. The game has been cancelled. 😢")
            return

        players = view.players
        self.active_games[ctx.channel.id] = {"players": {p.id: 0 for p in players}, "rounds": rounds, "elimination": elimination}

        await ctx.send(f"🎤 **Game Starting!** {rounds} rounds, {'Elimination Mode' if elimination else 'Normal Mode'}!")

        for i in range(1, rounds + 1):
            if ctx.channel.id not in self.active_games:
                return  

            simon_says = random.choice([True, False])
            action = get_random_command()
            message = f"**Simon says {action}!**" if simon_says else f"**{action}!**"
            await ctx.send(f"🕹️ **Round {i}/{rounds}:** {message}")

            try:
                responses = await self._get_responses(ctx, players, action, simon_says)
                round_winners = self._update_scores(ctx.channel.id, responses, simon_says, elimination)
                
                if round_winners:
                    winner_mentions = ", ".join([f"<@{winner}>" for winner in round_winners])
                    await ctx.send(f"🏆 {winner_mentions} won this round!")

            except:
                await ctx.send("⏳ No one responded in time!")

            if elimination and len(self.active_games[ctx.channel.id]["players"]) <= 1:
                break  

        await self._end_game(ctx)

    async def _get_responses(self, ctx: commands.Context, players: List[discord.Member], action: str, simon_says: bool):
        """Collects valid responses from joined players only."""
        responses = {}

        def check(m):
            return m.channel == ctx.channel and m.author in players

        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=5.0)
                if msg.author.id not in responses:
                    responses[msg.author.id] = msg.content.lower()
        except:
            pass  

        return responses

    def _update_scores(self, channel_id: int, responses: Dict[int, str], simon_says: bool, elimination: bool):
        """Updates scores and announces round winners."""
        game = self.active_games[channel_id]
        players = game["players"]
        round_winners = []

        for user_id, response in responses.items():
            if not check_response(response, get_random_command(), simon_says):
                if elimination:
                    del players[user_id]
                continue  

            players[user_id] += 1
            round_winners.append(user_id)

        return round_winners

    async def _end_game(self, ctx: commands.Context):
        """Ends the game and displays the leaderboard."""
        if ctx.channel.id not in self.active_games:
            return

        game = self.active_games.pop(ctx.channel.id)
        players = game["players"]

        await ctx.send(f"🏆 **Game Over!**\n{format_leaderboard(players)}")

async def setup(bot: Red):
    await bot.add_cog(SimonSays(bot))
