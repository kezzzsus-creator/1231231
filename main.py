import discord
from discord.ext import commands, tasks
import os

# Włącz intents – bez tego bot nie widzi członków / aktualizacji nicków
intents = discord.Intents.default()
intents.members = True          # ważne dla guildMemberUpdate i get_member

bot = commands.Bot(command_prefix='!', intents=intents)   # ← TO JEST KLUCZOWA LINIA! Tworzy 'bot'

TARGET_USER_ID = 385459721139650561   # ← zmień na ID tej osoby (PPM → Copy User ID)
FORCED_NICK = "Brudny Murzyn"   # ← Twój wymuszony nick

@bot.event
async def on_ready():
    print(f'Bot {bot.user} jest online i zaczyna lock nicku!')

@tasks.loop(seconds=10)  # sprawdza co 10 sekund – możesz dać 5, ale nie za często (rate-limit)
async def enforce_nick():
    # Zakładamy, że bot jest tylko na 1 serwerze – jeśli więcej, zmień na konkretne guild.id
    if not bot.guilds:
        return
    guild = bot.guilds[0]
    member = guild.get_member(TARGET_USER_ID)
    if member is None:
        print("Osoba nie znaleziona na serwerze – sprawdź czy jest online / bot ma uprawnienia")
        return
    
    if member.nick != FORCED_NICK:
        try:
            await member.edit(nick=FORCED_NICK)
            print(f'Resetowano nick {member} → {FORCED_NICK}')
        except discord.Forbidden:
            print("Błąd: Bot nie ma permisji Manage Nicknames LUB jest za nisko w hierarchii ról!")
        except Exception as e:
            print(f"Inny błąd: {e}")

# Natychmiastowy reset przy każdej zmianie nicku (najlepsze połączenie)
@bot.event
async def on_member_update(before, after):
    if after.id == TARGET_USER_ID and after.nick != FORCED_NICK:
        try:
            await after.edit(nick=FORCED_NICK)
            print(f"Szybki reset nicku dla {after} (on_member_update)")
        except Exception as e:
            print(f"Błąd w on_member_update: {e}")

# Start loopa po zalogowaniu
@bot.event
async def on_ready():
    print(f'Bot {bot.user} jest online!')
    enforce_nick.start()   # uruchamia cykliczne sprawdzanie

# Uruchomienie bota
token = os.getenv("DISCORD_TOKEN")
if token is None:
    print("BŁĄD: DISCORD_TOKEN nie znaleziono!")
    exit(1)

print("DISCORD_TOKEN z env:", token)
print("Typ:", type(token))

bot.run(token)
