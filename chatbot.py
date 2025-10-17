import random
import re
import discord

# Simple responses (you can add more)
responses = {
    "hello": ["Hey 👋", "Hi!", "What's up? 😎"],
    "how are": ["I'm good, thanks for asking 😄", "Doing okay, and you?", "Great as always 😎"],
    "who are you": ["I'm Legend Bot 🤖", "I'm your server bot!"],
    "what are you doing": ["Just hanging out 😁", "Waiting for your messages 🙃"],
    "help": ["You can use !topic or !rps ✨", "Just ask me something 😄"]
}

def get_response(message: str) -> str:
    msg = message.lower()
    for keyword, reply_list in responses.items():
        if re.search(rf"\b{keyword}\b", msg):
            return random.choice(reply_list)

    # Fallback response
    fallback = [
        "Hmm… I didn't quite get that 🤔",
        "Interesting 😄",
        "Tell me more 👀",
        "Sounds exciting!"
    ]
    return random.choice(fallback)

async def handle_message(message: discord.Message):
    if message.author.bot:
        return  # Ignore other bots

    # Only respond if bot is mentioned
    if message.mentions and message.guild.me in message.mentions:
        content = message.content.replace(f"<@{message.guild.me.id}>", "").strip()
        if content:
            response = get_response(content)
            await message.reply(response)