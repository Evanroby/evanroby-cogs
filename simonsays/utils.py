import random
from typing import Dict, List

def get_random_command() -> str:
    """Returns a random Simon Says command."""
    actions = ["jump", "wave", "clap", "spin", "sit", "dance"]
    return random.choice(actions)

def format_leaderboard(players: Dict[int, int]) -> str:
    """Formats the leaderboard into a Discord-friendly string."""
    if not players:
        return "No winners this time. 😢"

    sorted_players = sorted(players.items(), key=lambda x: x[1], reverse=True)
    return "\n".join([f"🥇 **<@{p[0]}>** - {p[1]} points" for p in sorted_players])

def check_response(user_response: str, action: str, simon_says: bool) -> bool:
    """Checks if the user followed Simon's instructions correctly."""
    correct_phrase = f"simon says {action}"
    return (simon_says and correct_phrase in user_response.lower()) or (not simon_says and correct_phrase not in user_response.lower())
