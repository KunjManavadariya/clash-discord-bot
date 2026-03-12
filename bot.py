import discord
import requests
from discord.ext import commands, tasks
from datetime import datetime

TOKEN = "MTQ4MTYzMDIyMjU5MDY3Mjk0OA.Go1oOr.ZjEMn-5vIp3Jg7KVlHyB08gBswzQ4cw1qVBttw"
COC_API = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImM0Y2FjYTljLTI0Y2ItNGI4ZS05NDEzLWIzNzFjNjQzYzYxMyIsImlhdCI6MTc3MzMyMDQ2Miwic3ViIjoiZGV2ZWxvcGVyLzU5OGQzNGE0LTY4YWEtNmZmYy04NGExLWQ0M2M1MDllYWMwYiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwNi4yMDEuMjMwLjIyMiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.mGIVg6nWGag0PJoGdO9WuYUQlL6LR4vwyDzT9y5Kzsr7A32SrU6EGLTnAvp7aylQOssl9j-BeDaGKnFF0o88MA"
CLAN_TAG = "%2382RRUUUU"

TROPHY_CHANNEL = 1037779646101594122   # channel ID

headers = {"Authorization": f"Bearer {COC_API}"}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

leaderboard_message = None


@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")
    trophy_update.start()


@tasks.loop(minutes=10)
async def trophy_update():

    global leaderboard_message

    url = f"https://api.clashofclans.com/v1/clans/{CLAN_TAG}/members"

    try:
        r = requests.get(url, headers=headers)
        data = r.json()
    except Exception as e:
        print("Request failed:", e)
        return

    if "items" not in data:
        print("API Error:", data)
        return

    players = sorted(data["items"], key=lambda x: x["trophies"], reverse=True)

    msg = "🏆 **Clan Trophy Rankings**\n\n"

    for i, player in enumerate(players[:50]):
        msg += f"{i+1}. {player['name']} — {player['trophies']}🏆\n"

    msg += f"\n🕒 Last Updated: {datetime.utcnow().strftime('%H:%M UTC')}"

    channel = bot.get_channel(TROPHY_CHANNEL)

    if channel is None:
        print("Channel not found")
        return

    try:

        # First time send message
        if leaderboard_message is None:
            leaderboard_message = await channel.send(msg)

        # After that edit message
        else:
            await leaderboard_message.edit(content=msg)

    except Exception as e:
        print("Discord error:", e)


bot.run(TOKEN)