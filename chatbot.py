import random
import re
import discord

# Einfache Antworten (du kannst hier beliebig viele hinzufügen)
responses = {
    "hallo": ["Hey 👋", "Hi!", "Na, wie geht’s?", "Servus 😎"],
    "wie geht": ["Mir geht's gut, danke der Nachfrage 😄", "Ganz okay, und dir?", "Top wie immer 😎"],
    "wer bist du": ["Ich bin der Legend Bot 🤖", "Ich bin euer Server-Bot!"],
    "was machst du": ["Ich häng hier rum 😁", "Warte auf eure Nachrichten 🙃"],
    "hilfe": ["Du kannst !topic oder !rps verwenden ✨", "Frag mich einfach was 😄"]
}

def get_response(message: str) -> str:
    msg = message.lower()

    for keyword, reply_list in responses.items():
        if re.search(rf"\b{keyword}\b", msg):
            return random.choice(reply_list)

    # Standard Antwort, falls kein Keyword gefunden wurde
    fallback = [
        "Hmm… das hab ich nicht ganz verstanden 🤔",
        "Interessant 😄",
        "Erzähl mir mehr 👀",
        "Das klingt spannend!"
    ]
    return random.choice(fallback)

async def handle_message(message: discord.Message):
    if message.author.bot:
        return  # Bot soll nicht auf sich selbst antworten

    content = message.content.strip()

    # Wenn der Bot erwähnt wird oder jemand direkt schreibt
    if message.mentions and message.guild.me in message.mentions:
        response = get_response(content)
        await message.reply(response)
    else:
        # Reagiert auch auf ganz normale Nachrichten (optional)
        # Wenn du das nicht willst, einfach diesen Teil auskommentieren
        response = get_response(content)
        if response:
            await message.channel.send(response)