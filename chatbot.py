import random
import discord
import re
from collections import deque
from rps import start_rps_game  # Deine RPS-Funktion
from topic import topics  # <- Importiere deine Liste aus topic.py

# ======================
# Keyword-Response Mapping
# ======================
responses = {
    # ===== Priority 1: Greetings =====
    r"\bhi\b|\bhello\b|\bhey\b|\byo\b|\bhiya\b|\bgreetings\b|\bwhat's up\b|\bhowdy\b": [
        "Hey there! 👋",
        "Hello! How’s it going?",
        "Hi! Nice to see you here!",
        "Yo! How’s your day?",
        "Hiya! What’s up?",
        "Greetings! 😄",
        "Hey hey! 😎",
        "Hello friend! 😊"
    ] * 20,

    # ===== Priority 2: Mood / Feelings =====
    r"\bhow are you(\sdoing)?\b|\bhow's it going\b|\bwhat's up\b|\bsup\b|\bhow do you do\b|\bhow r u\b": [
        "I’m doing great, thanks! 😄 How about you?",
        "Pretty chill 😎, how about you?",
        "All good! How’s your day going?",
        "Feeling awesome today! What about you?",
        "I’m fine! What are you up to?",
        "Doing well! Ready for some chat? 😁"
    ] * 20,

    r"\bfeel good\b|\bhappy\b|\bexcited\b|\blucky\b": [
        "That’s awesome! 😄",
        "Glad to hear that! Keep it up! 🌟",
        "Happy vibes! ✨",
        "Nice! What’s making you feel good today?"
    ] * 20,

    r"\bbored\b|\btired\b|\blonely\b|\bsad\b": [
        "Oh no! 😢 How about a game to cheer you up? Type `!rps` for a normal round or `!rps_bo3` for Best of 3! 🕹️",
        "Maybe a game will help! 😏 Use `!rps` or `!rps_bo3` and we can start right away!",
        "I'm here to cheer you up! Want to play a round of Rock Paper Scissors? `!rps` or `!rps_bo3`",
        "Cheer up! 😄 Let's play! Type `!rps` for a simple round or `!rps_bo3` for Best of 3!"
    ] * 20,

    # ===== Priority 3: Games / Fun =====
    r"\bwanna play\b|\bgame\b|\bplay something\b|\brps\b|\bchallenge\b": [
        "I’d love to play! 😄 Use `!rps` for a normal round or `!rps_bo3` for Best of 3!",
        "Games sound fun! Just type `!rps` or `!rps_bo3` to start!",
        "Ready to challenge me? 😏 Use `!rps` or `!rps_bo3`!",
        "I can’t start the game here 😅, but type `!rps` or `!rps_bo3`!"
    ] * 20,

    # ===== Priority 4: Help / Commands =====
    r"\bcan you help me\b|\bhelp\b|\bwhat can i do\b|\binstructions\b|\bguide\b": [
        "Sure! Try commands like `!topic`, `!rps`, or `!rps_bo3` 🎲",
        "I can explain commands if you want! 😄",
        "Ask me anything, I’ll do my best to answer!",
        "Commands like `!topic`, `!rps`, or `!info` work great!"
    ] * 20,

    # ===== Priority 5: Smalltalk / Reactions =====
    r"\blol\b|\bhaha\b|\blmao\b|\bfunny\b|\bamazing\b|\bcool\b|\bwow\b|\bnice\b|\bgreat\b": [
        "Haha, that’s funny 😄",
        "Lmao, totally!",
        "🤣 I can relate!",
        "Wow indeed! 😲",
        "That’s really cool! 😎"
    ] * 20,

    # ===== Priority 6: Trivia / Fun =====
    r"\btell me a joke\b|\banother joke\b|\btell me an interesting fact\b|\binteresting fact\b": [
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
        "Fun fact: Octopuses have three hearts! 🐙",
        "Did you know? Bananas are berries! 🍌",
        "Why don’t scientists trust atoms? Because they make up everything! 😆"
    ] * 20,

    # ===== Priority 7: Greetings / Tageszeit =====
    r"\bgood morning\b|\bmorning\b": [
        "Good morning! ☀️ Ready for a great day?",
        "Morning! How’s it going so far?",
        "Hey! Have an awesome morning! 😄"
    ],
    r"\bgood night\b|\bnight\b|\bgn\b": [
        "Good night! 🌙 Sleep tight!",
        "Sweet dreams! 😌",
        "Nighty night! See you tomorrow! 🛌"
    ],

    # ===== Priority 8: Identity / About Bot =====
    r"\bwho are you\b|\bwhat are you\b|\bintroduce yourself\b": [
        "I'm Legend Bot, your friendly server companion! 😎",
        "I’m a bot made to chat, play games, and have fun with you! 🤖",
        "They call me Legend Bot! Here to make your day more fun!",
        "Just your friendly neighborhood bot, always ready to chat!",
        "I’m Legend Bot! I can chat, tell jokes, and even play Rock Paper Scissors!",
        "A bot with great taste in games and conversations 😏",
        "Legend Bot at your service! Here to entertain and assist!"
    ] * 20,

    # ===== Priority 9: Topics =====
    r"\bgive me a topic\b|\btopic\b": [
        lambda: random.choice(topics)
    ],

    # ===== Priority 10: Fallback =====
    r".*": [
        "Hmm… I didn't quite get that 🤔",
        "Interesting 😄",
        "Tell me more 👀",
        "Sounds exciting!",
        "Oh really? That’s cool!",
        "Can you elaborate a bit?",
        "Haha, I get it 😄"
    ] * 50
}

# ======================
# Store last messages per channel for context
# ======================
last_messages = {}  # key = channel id, value = deque(maxlen=5)

# ======================
# Function to get response
# ======================
def get_response(message: str, channel_id: int = 0) -> str:
    msg = message.lower()

    # Kontext speichern
    if channel_id not in last_messages:
        last_messages[channel_id] = deque(maxlen=5)
    last_messages[channel_id].append(msg)

    # Suche nach Keywords
    for pattern, replies in responses.items():
        if re.search(pattern, msg):
            reply = random.choice(replies)
            if callable(reply):  # Falls es eine Funktion ist (wie bei Topics)
                return reply()
            return reply

    return random.choice(responses[r".*"])

# ======================
# Handle Discord Messages
# ======================
async def handle_message(message: discord.Message):
    if message.author.bot:
        return

    # Nur reagieren, wenn @Bot erwähnt wird
    if message.mentions and message.guild.me in message.mentions:
        content = re.sub(f"<@!?{message.guild.me.id}>", "", message.content).strip()

        # === Wenn User "yes" sagt, sage nur, welche Commands existieren ===
        if content.lower() == "yes":
            await message.reply("Type `!rps` for a normal round or `!rps_bo3` for Best of 3! 🕹️")
            return  # Keine andere Antwort senden

        # Normale Keyword-Antwort
        response = get_response(content, message.channel.id)
        await message.reply(response)