import os

token = os.getenv("DISCORD_TOKEN")
print("DISCORD_TOKEN z env:", token)           # ← to się pojawi w logach
print("Typ:", type(token))                     # ← powinno być <class 'str'> a nie NoneType

if token is None:
    print("BŁĄD: DISCORD_TOKEN nie znaleziono w zmiennych środowiskowych!")
    exit(1)  # kończy działanie, żeby nie próbować logować z None

bot.run(token)
