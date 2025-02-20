import discord
import random
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import bold
from typing import Dict, Optional

class SimonSays(commands.Cog):
    """A fun Simon Says game with scoring, rounds, and elimination mode!"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.active_games = {}

    @commands.hybrid_command(name="simonsays", with_app_command=True)
    async def simonsays(self, ctx: commands.Context, rounds: Optional[int] = 5, elimination: Optional[bool] = False):
        """
        Start a Simon Says game!
        - `rounds`: Number of rounds (default: 5)
        - `elimination`: Set to True for elimination mode
        """
        if ctx.channel.id in self.active_games:
            await ctx.send("A Simon Says game is already running in this channel!")
            return

        self.active_games[ctx.channel.id] = {"players": {}, "rounds": rounds, "elimination": elimination}

        await ctx.send(f"🎤 **Simon Says** is starting! {rounds} rounds, {'Elimination Mode' if elimination else 'Normal Mode'}!")

        for i in range(1, rounds + 1):
            if ctx.channel.id not in self.active_games:
                return  

            simon_says = random.choice([True, False])
            action = random.choice(["jump", "wave", "clap", "spin", "sit", "dance"])
            message = f"**Simon says {action}!**" if simon_says else f"**{action}!**"
            await ctx.send(f"🕹️ Round {i}/{rounds}: {message}")

            try:
                responses = await self._get_responses(ctx, action, simon_says)
                self._update_scores(ctx.channel.id, responses, simon_says, elimination)
            except:
                await ctx.send("⏳ No one responded in time!")

            if elimination and len(self.active_games[ctx.channel.id]["players"]) <= 1:
                break  

        await self._end_game(ctx)

    @commands.command(name="simonsays_prefix")
    async def simonsays_prefix(self, ctx: commands.Context, rounds: Optional[int] = 5, elimination: Optional[bool] = False):
        """Start Simon Says using a prefix command."""
        await self.simonsays(ctx, rounds, elimination)

    async def _get_responses(self, ctx: commands.Context, action: str, simon_says: bool):
        """Collects player responses and returns valid ones."""
        responses = {}

        def check(m):
            return m.channel == ctx.channel and m.author != self.bot

        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=5.0)
                if msg.author.id not in responses:  
                    responses[msg.author.id] = msg.content.lower()
        except:
            pass  

        return responses

    def _update_scores(self, channel_id: int, responses: Dict[int, str], simon_says: bool, elimination: bool):
        """Updates scores and handles elimination mode."""
        game = self.active_games[channel_id]
        players = game["players"]

        for user_id, response in responses.items():
            if simon_says and response != "simon says":
                if elimination:
                    del players[user_id]
                continue  

            if not simon_says and response == "simon says":
                if elimination:
                    del players[user_id]
                continue 

            if user_id in players:
                players[user_id] += 1
            else:
                players[user_id] = 1

    async def _end_game(self, ctx: commands.Context):
        """Ends the game and displays the leaderboard."""
        if ctx.channel.id not in self.active_games:
            return

        game = self.active_games.pop(ctx.channel.id)
        players = game["players"]

        if not players:
            await ctx.send("Game over! No one won this time. 😢")
            return

        leaderboard = sorted(players.items(), key=lambda x: x[1], reverse=True)
        results = "\n".join([f"🥇 **<@{p[0]}>** - {p[1]} points" for p in leaderboard])
        await ctx.send(f"🏆 **Game Over!**\n{results}")

    @commands.hybrid_command(name="stop_simon", with_app_command=True)
    async def stop_simon(self, ctx: commands.Context):
        """Stops the ongoing Simon Says game."""
        if ctx.channel.id in self.active_games:
            del self.active_games[ctx.channel.id]
            await ctx.send("❌ Simon Says game has been stopped.")
        else:
            await ctx.send("No Simon Says game is currently running.")

    @commands.command(name="stop_simon_prefix")
    async def stop_simon_prefix(self, ctx: commands.Context):
        """Stops the Simon Says game using a prefix command."""
        await self.stop_simon(ctx)

async def setup(bot: Red):
    await bot.add_cog(SimonSays(bot))
