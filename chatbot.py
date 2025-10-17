import random
import re
import discord

import random
import discord

# ===== Extensive Keyword-Response Mapping =====
responses = {
    # Greetings
    "hi|hello|hey|yo|hiya": [
        "Hey there! 👋",
        "Hello! How’s it going?",
        "Hi! Nice to see you here!",
        "Yo! How’s your day?",
        "Hiya! What’s up?"
    ],
    # How are you
    "how are you|how's it going|what's up|sup": [
        "I’m doing great, thanks for asking! 😄",
        "Pretty chill 😎, how about you?",
        "All good! How’s your day going?",
        "Feeling awesome today! What about you?",
        "Doing well, thanks! What are you up to?"
    ],
    # Good morning/night
    "good morning|morning": [
        "Good morning! ☀️",
        "Morning! Ready for a new day?",
        "Hey! Have a great morning!"
    ],
    "good night|night|gn": [
        "Good night! 🌙",
        "Sleep well! 😴",
        "Sweet dreams! 😌"
    ],
    # Who / What
    "who are you|what are you": [
        "I’m Legend Bot 🤖",
        "I’m your friendly server bot!",
        "Just a bot trying to keep things fun 😎"
    ],
    # Small talk / casual
    "what's your favorite game|favorite game": [
        "I love playing Rock Paper Scissors 😏",
        "Hmm… I’m a fan of chess and card games!",
        "I enjoy online games with you guys!"
    ],
    "what's your favorite movie|favorite movie": [
        "I like all the Marvel movies 🦸‍♂️",
        "Inception is my favorite, mind-blowing!",
        "Star Wars forever! 🚀"
    ],
    "what's your favorite food|favorite food": [
        "Pizza is the best 🍕",
        "I’m a fan of sushi 🍣",
        "Chocolate, always chocolate 🍫"
    ],
    "do you like music|favorite song|music": [
        "I enjoy chill lo-fi beats 😎",
        "Pop and rock are my favorites!",
        "Anything with a good rhythm 🎵"
    ],
    "hobbies|what do you do|free time": [
        "I love chatting with you guys!",
        "Sometimes I play Rock Paper Scissors 😏",
        "I enjoy observing conversations!"
    ],
    # Reactions
    "lol|haha|lmao|funny": [
        "Haha, that’s funny 😄",
        "Lmao, totally!",
        "🤣 I can relate!"
    ],
    "wow|amazing|cool": [
        "Wow indeed! 😲",
        "That’s really cool! 😎",
        "I like that!"
    ],
    "oh no|oops|uh oh": [
        "Uh oh… 😬",
        "Be careful! 😅",
        "That sounds tricky!"
    ],
    # Questions / curiosity
    "how do you|can you|what is|tell me": [
        "Hmm… let me think 🤔",
        "Interesting question!",
        "I don’t know everything, but I’ll try!"
    ],
    # Fun / Random
    "joke|funny|make me laugh": [
        "Why did the scarecrow win an award? Because he was outstanding in his field! 😆",
        "I would tell you a joke about time… but you’ll have to wait! ⏳",
        "I tried to catch fog yesterday… Mist!"
    ],
    "game|play": [
        "I can play Rock Paper Scissors with you! 🕹️",
        "Want to start a mini game?",
        "I love fun games, let’s go!"
    ],
    "weather|sun|rain|cold|hot": [
        "I hope it’s sunny where you are! ☀️",
        "Rainy days are cozy 🌧️",
        "Stay warm if it’s cold out there!"
    ],
    "travel|holiday|vacation": [
        "I’d love to visit Japan one day 🇯🇵",
        "A beach vacation sounds nice! 🏖️",
        "Mountains or beach? Tough choice!"
    ],
    "animal|pet|dog|cat": [
        "I love dogs! 🐶",
        "Cats are mysterious and cute 😸",
        "I like all kinds of animals 🐾"
    ],
    "favorite color|color": [
        "I really like neon blue and purple! 💜💙",
        "Green is pretty nice 🌿",
        "Red is always bold 🔴"
    ],
    "book|reading": [
        "I enjoy sci-fi books! 🚀",
        "Fantasy worlds are so cool 🧙‍♂️",
        "I love short stories!"
    ],
    "food|drink": [
        "Coffee is great ☕",
        "Tea is relaxing 🍵",
        "Pizza forever! 🍕"
    ],
    "study|work|job|career": [
        "I’m just a bot, so chatting is my job 😏",
        "Work hard, relax harder!",
        "Learning new stuff is always fun!"
    ],
    "happy|fun|excited": [
        "Yay! That’s awesome 😄",
        "Sounds fun! 🎉",
        "I’m happy to hear that!"
    ],
    "sad|angry|upset": [
        "Oh no… 😢",
        "That sucks 😔",
        "Hope things get better soon!"
    ]
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
        "Sounds exciting!",
        "Oh really? That’s cool!",
        "Can you elaborate a bit?",
        "I see… tell me more!",
        "Haha, I get it 😄",
        "That’s funny!",
        "True true 😌"
    ]
    return random.choice(fallback)

# ===== Handle Discord Messages =====
async def handle_message(message: discord.Message):
    if message.author.bot:
        return

    if message.mentions and message.guild.me in message.mentions:
        content = message.content.replace(f"<@{message.guild.me.id}>", "").strip()
        if content:
            response = get_response(content)
            await message.reply(response)