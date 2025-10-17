import random
import re
import discord

# ===== Keyword-Responses Mapping =====
responses = {
    # Greetings
    "hi|hello|hey": [
        "Hey there! How’s everything going today?",
        "Hi! 👋",
        "Hello! How’s it going?"
    ],
    # How are you
    "how are you|how's it going|what's up": [
        "I’m good, thanks for asking! 😄",
        "Pretty chill 😎, how about you?",
        "Doing well! What about you?"
    ],
    # Good morning/night
    "good morning": ["Good morning! ☀️", "Morning! Hope you have a great day!"],
    "good night": ["Good night! 🌙", "Sleep well! 😴"],
    # Misc casual
    "who are you": ["I’m Legend Bot 🤖", "I’m your friendly server bot!"],
    "what are you doing|what's up": ["Just hanging around 😁", "Waiting for your messages 🙃"],
    "help": ["You can try !topic or !rps ✨", "Just ask me anything! 😄"]
}

# ===== Function to get response =====
def get_response(message: str) -> str:
    msg = message.lower()
    for keyword_pattern, reply_list in responses.items():
        if any(kw.strip() in msg for kw in keyword_pattern.split("|")):
            return random.choice(reply_list)
    
    # Fallback Antwort
    fallback = [
        "Hmm… I didn't quite get that 🤔",
        "Interesting 😄",
        "Tell me more 👀",
        "Sounds exciting!"
    ]
    return random.choice(fallback)

# ===== Handle Discord Messages =====
async def handle_message(message: discord.Message):
    if message.author.bot:
        return  # Bot antwortet nicht auf sich selbst

    # Nur reagieren, wenn der Bot erwähnt wird
    if message.mentions and message.guild.me in message.mentions:
        content = message.content.replace(f"<@{message.guild.me.id}>", "").strip()
        if content:
            response = get_response(content)
            await message.reply(response)