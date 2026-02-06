import discord
from discord.ext import commands, tasks
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_USER_ID = 385459721139650561   # Twoje ID osoby docelowej
FORCED_NICK = "Brudny Murzyn"   # Zmień na co chcesz

@bot.event
async def on_ready():
    print(f'Bot {bot.user} jest online!')
    enforce_nick.start()

@tasks.loop(seconds=10)  # co 10 sekund – możesz dać 5
async def enforce_nick():
    guild = bot.guilds[0]  # zakładając 1 serwer; możesz zmienić
    member = guild.get_member(TARGET_USER_ID)
    if member and member.nick != FORCED_NICK:
        try:
            await member.edit(nick=FORCED_NICK)
            print(f'Reset nicku dla {member}')
        except Exception as e:
            print(e)

@bot.event
async def on_member_update(before, after):
    if after.id == TARGET_USER_ID and after.nick != FORCED_NICK:
        try:
            await after.edit(nick=FORCED_NICK)
            print("Szybki reset na zmianę!")
        except:
            pass

bot.run(os.getenv("DISCORD_TOKEN"))
