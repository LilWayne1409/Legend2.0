import random
import discord
import re

# ======================
# Keyword-Response Mapping
# ======================
responses = {
# ===== Priorität 1: Stimmung / Wie geht's =====
r"\bhow are you(\sdoing)?\b|\bhow's it going\b|\bwhat's up\b|\bsup\b|\bhow do you do\b": [
    "I’m doing great, thanks! 😄",
    "Pretty chill 😎, how about you?",
    "All good! How’s your day going?",
    "Feeling awesome today! What about you?",
    "I’m fine! What are you up to?"
    ],
    r"\bwho are you\b|\bwhat are you\b": [
        "I’m Legend Bot 🤖",
        "I’m your friendly server bot!",
        "Just a bot trying to keep things fun 😎"
    ],
    r"\bwhat's your favorite game\b|\bfavorite game\b": [
        "I love playing Rock Paper Scissors 😏",
        "Hmm… I’m a fan of chess and card games!",
        "I enjoy online games with you guys!"
    ],
    r"\bwhat's your favorite movie\b|\bfavorite movie\b": [
        "I like all the Marvel movies 🦸‍♂️",
        "Inception is my favorite, mind-blowing!",
        "Star Wars forever! 🚀"
    ],
    r"\bwhat's your favorite food\b|\bfavorite food\b": [
        "Pizza is the best 🍕",
        "I’m a fan of sushi 🍣",
        "Chocolate, always chocolate 🍫"
    ],
    r"\bdo you like music\b|\bfavorite song\b|\bmusic\b": [
        "I enjoy chill lo-fi beats 😎",
        "Pop and rock are my favorites!",
        "Anything with a good rhythm 🎵"
    ],
    r"\bhobbies\b|\bwhat do you do\b|\bfree time\b": [
        "I love chatting with you guys!",
        "Sometimes I play Rock Paper Scissors 😏",
        "I enjoy observing conversations!"
    ],

    # ===== Priority 2: Greetings =====
    r"\bhi\b|\bhello\b|\bhey\b|\byo\b|\bhiya\b": [
        "Hey there! 👋",
        "Hello! How’s it going?",
        "Hi! Nice to see you here!",
        "Yo! How’s your day?",
        "Hiya! What’s up?"
    ],
    r"\bgood morning\b|\bmorning\b": [
        "Good morning! ☀️",
        "Morning! Ready for a new day?",
        "Hey! Have a great morning!"
    ],
    r"\bgood night\b|\bnight\b|\bgn\b": [
        "Good night! 🌙",
        "Sleep well! 😴",
        "Sweet dreams! 😌"
    ],

    # ===== Priority 3: Smalltalk / Reactions =====
    r"\blol\b|\bhaha\b|\blmao\b|\bfunny\b": [
        "Haha, that’s funny 😄",
        "Lmao, totally!",
        "🤣 I can relate!"
    ],
    r"\bwow\b|\bamazing\b|\bcool\b": [
        "Wow indeed! 😲",
        "That’s really cool! 😎",
        "I like that!"
    ],
    r"\boh no\b|\boops\b|\buh oh\b": [
        "Uh oh… 😬",
        "Be careful! 😅",
        "That sounds tricky!"
    ],

    # ===== Priority 4: Games / Fun =====
    r"\bwanna play\b|\bgame\b|\bplay something\b": [
        "Sure! Let’s play Rock Paper Scissors! ✂️🪨📄",
        "I’m always up for a game! Want to try !rps?",
        "Games sound fun! How about a quick match?",
        "Yes! I can challenge you to something fun 😏"
    ],

    # ===== Priority 5: Help / Commands =====
    r"\bcan you help me\b|\bhelp\b|\bwhat can i do\b": [
        "Sure! You can try commands like !topic or !rps 🎲",
        "Of course! Ask me anything, I’ll try to answer 😄",
        "Absolutely! I can start a game, give a topic, or just chat!",
        "Yep! You can ping me or play a game like Rock Paper Scissors!"
    ],

    # ===== Fallback =====
    r".*": [
        "Hmm… I didn't quite get that 🤔",
        "Interesting 😄",
        "Tell me more 👀",
        "Sounds exciting!",
        "Oh really? That’s cool!",
        "Can you elaborate a bit?",
        "I see… tell me more!",
        "Haha, I get it 😄",
        "That’s funny!",
        "True true 😌"
    ]
}

# ===== Function to get response =====
def get_response(message: str) -> str:
    msg = message.lower()
    for pattern, replies in responses.items():
        if re.search(pattern, msg):
            return random.choice(replies)
    # Fallback
    return random.choice(responses[r".*"])

# ===== Handle Discord Messages =====
async def handle_message(message: discord.Message):
    if message.author.bot:
        return

    # Nur reagieren, wenn @Bot erwähnt wird
    if message.mentions and message.guild.me in message.mentions:
        # Erwähnung entfernen
        content = re.sub(f"<@!?{message.guild.me.id}>", "", message.content).strip()
        if content:
            response = get_response(content)
            await message.reply(response)