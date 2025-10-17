import random
import discord
import re

# ===== Extensive Keyword-Response Mapping =====
responses = {
    # Priorität 1: Specific / Detailed
    r"\bhow are you\b|\bhow's it going\b|\bwhat's up\b|\bsup\b": [
        "I’m doing great, thanks! 😄",
        "Pretty chill 😎, how about you?",
        "All good! How’s your day going?",
        "Feeling awesome today! What about you?",
        "Doing well, thanks! What are you up to?"
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

    # Priorität 2: Greetings
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

    # Priorität 3: Reactions / Small Talk
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

    # Priorität 4: Fallback / Random
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
    return "Hmm… I didn't quite get that 🤔"

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