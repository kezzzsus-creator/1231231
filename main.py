import discord
from discord.ext import commands, tasks
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_USER_ID = 385459721139650561
FORCED_NICK = "Brrrrrr"

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
            print(f'Osoba znaleziona! Aktualny nick: {member.nick or "brak nicku (używa globalnego)"}')
            print(f'ID osoby zgadza się: {member.id == TARGET_USER_ID}')
        else:
            print('!!! OSOBA NIE ZNALEZIONA W CACHE !!! (bot jej nie widzi)')
    else:
        print('Bot nie jest na żadnym serwerze?')

    enforce_nick.start()

@tasks.loop(seconds=8)
async def enforce_nick():
    print('[LOOP] Sprawdzam nick...')
    if not bot.guilds:
        print('[LOOP] Brak serwera')
        return
    
    guild = bot.guilds[0]
    member = guild.get_member(TARGET_USER_ID)
    if member is None:
        print('[LOOP] Członek NIE znaleziony!')
        return
    
    current_nick = member.nick
    print(f'[LOOP] Aktualny nick: {current_nick or "brak"}')
    
    if current_nick != FORCED_NICK:
        print(f'[LOOP] Nick inny → próbuję ustawić "{FORCED_NICK}"')
        try:
            await member.edit(nick=FORCED_NICK)
            print(f'[LOOP] SUKCES – nick zmieniony!')
        except discord.Forbidden:
            print('[LOOP] FORBIDDEN – brak permisji lub rola bota za nisko!')
        except discord.HTTPException as exc:
            print(f'[LOOP] HTTP błąd: {exc.status} – {exc.text}')
        except Exception as e:
            print(f'[LOOP] Inny błąd: {type(e).__name__} → {e}')
    else:
        print('[LOOP] Nick już poprawny')

@bot.event
async def on_member_update(before, after):
    print('[EVENT] on_member_update odpalił!')
    if after.id != TARGET_USER_ID:
        return
    
    print(f'[EVENT] Zmiana nicku u osoby! Przed: {before.nick} → Po: {after.nick}')
    if after.nick != FORCED_NICK:
        print('[EVENT] Resetuję natychmiast!')
        try:
            await after.edit(nick=FORCED_NICK)
            print('[EVENT] Szybki reset → UDANY')
        except Exception as e:
            print(f'[EVENT] Błąd resetu: {e}')

token = os.getenv("DISCORD_TOKEN")
if token is None:
    print("Brak tokenu!")
    exit(1)

print("Token OK:", token[:10] + "...")
bot.run(token)
