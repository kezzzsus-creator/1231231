import discord
from discord.ext import commands, tasks
import os
import random
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_USER_ID = 385459721139650561

NICKNAMES = [
    "Brudny Murzyn 💩👨🏿‍🦱",
    "Ludzki pisuar 🚽💩",
    "Skazany na anal 🍑🍆",
    "Analna niewolnica ojczyma",
    "Skarpeta Epsteina 🧦🧴"
]

MIN_INTERVAL = 5
MAX_INTERVAL = 10

current_forced_nick = random.choice(NICKNAMES)

@bot.event
async def on_ready():
    print(f'=== BOT ONLINE === {bot.user}')
    print(f'Liczba serwerów: {len(bot.guilds)}')
    
    if bot.guilds:
        guild = bot.guilds[0]
        print(f'Serwer: {guild.name} ({guild.id})')
        print(f'Bot ma Manage Nicknames? → {guild.me.guild_permissions.manage_nicknames}')
        print(f'Pozycja roli bota: {guild.me.top_role.position}')
        
        member = guild.get_member(TARGET_USER_ID)
        if member:
            print(f'Osoba znaleziona! Aktualny nick: {member.nick or "brak nicku"}')
        else:
            print('!!! OSOBA NIE ZNALEZIONA W CACHE !!!')
    else:
        print('Bot nie jest na żadnym serwerze?')

    enforce_nick.start()


@tasks.loop(seconds=7)  # baza, ale zmieniamy dynamicznie co iterację
async def enforce_nick():
    global current_forced_nick

    # Losujemy nowy odstęp czasu na następne wywołanie
    next_delay = random.uniform(MIN_INTERVAL, MAX_INTERVAL)
    enforce_nick.change_interval(seconds=next_delay)

    print(f'[LOOP] Sprawdzam nick... (następne sprawdzenie za ~{next_delay:.1f}s)')

    if not bot.guilds:
        print('[LOOP] Brak serwera')
        return
    
    guild = bot.guilds[0]
    member = guild.get_member(TARGET_USER_ID)
    if member is None:
        print('[LOOP] Członek NIE znaleziony!')
        return
    
    current_nick = member.nick or ""   # traktujemy brak nicku jako pusty string

    
    current_forced_nick = random.choice(NICKNAMES)
    
    if current_nick != current_forced_nick:
        print(f'[LOOP] Ustawiam nowy nick → "{current_forced_nick}"')
        try:
            await member.edit(nick=current_forced_nick)
            print(f'[LOOP] SUKCES – nick zmieniony na "{current_forced_nick}"')
        except discord.Forbidden:
            print('[LOOP] FORBIDDEN – brak permisji lub rola bota za nisko!')
        except discord.HTTPException as exc:
            if exc.status == 429:
                print(f'[LOOP] Rate limit! Retry after: {exc.retry_after:.1f}s')
            else:
                print(f'[LOOP] HTTP {exc.status} – {exc.text}')
        except Exception as e:
            print(f'[LOOP] Błąd: {type(e).__name__} → {e}')
    else:
        print(f'[LOOP] Nick już jest "{current_forced_nick}" – bez zmian')


@bot.event
async def on_member_update(before, after):
    global current_forced_nick
    
    if after.id != TARGET_USER_ID:
        return
    
    current_nick = after.nick or ""
    
    if current_nick != current_forced_nick:
        print(f'[EVENT] Ktoś zmienił nick! Przed: {before.nick} → Po: {current_nick}')
        print(f'[EVENT] Natychmiast resetuję na "{current_forced_nick}"')
        try:
            await after.edit(nick=current_forced_nick)
            print('[EVENT] Szybki reset → UDANY')
        except Exception as e:
            print(f'[EVENT] Błąd resetu: {e}')


token = os.getenv("DISCORD_TOKEN")
if token is None:
    print("Brak tokenu!")
    exit(1)

print("Token OK:", token[:10] + "...")
bot.run(token)
