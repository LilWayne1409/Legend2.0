import random
import discord
import re
from collections import deque
from rps import start_rps_game  # Stelle sicher, dass deine rps.py diese Funktion hat

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
        "Hello friend! 😊",
        "Hi! How’s everything today?",
        "Yo! Long time no see!"
    ] * 20,

    # ===== Priority 2: Mood / Feelings =====
    r"\bhow are you(\sdoing)?\b|\bhow's it going\b|\bwhat's up\b|\bsup\b|\bhow do you do\b|\bhow r u\b": [
        "I’m doing great, thanks! 😄",
        "Pretty chill 😎, how about you?",
        "All good! How’s your day going?",
        "Feeling awesome today! What about you?",
        "I’m fine! What are you up to?",
        "Doing well! Ready for some chat? 😁",
        "I’m in a good mood today! 😎",
        "Chill and relaxed! How’s your day?",
        "Fantastic! How are you feeling?",
        "Hey! I’m having a nice day here."
    ] * 20,

    # ===== Priority 3: Hobbies & Activities =====
    r"\bwhat are you doing\b|\bwhatcha doing\b|\bfree time\b|\bhobbies\b|\bwhat do you do\b|\bwhat's up\b": [
        "Just hanging out here 😎",
        "Waiting for your messages! 😁",
        "Chillin’ and ready to chat! 🕹️",
        "I’m exploring the server! 👀",
        "Talking to awesome people like you!",
        "Playing some Rock Paper Scissors 😏",
        "Observing conversations is my hobby!",
        "Just relaxing here in the server 😌",
        "Looking for someone to challenge me to a game!",
        "Just scrolling and chatting! 😄"
    ] * 20,

    # ===== Priority 4: Favorites =====
    r"\bwhat's your favorite color\b|\bfavorite color\b|\bwhat's your favorite food\b|\bfavorite food\b|\bwhat's your favorite movie\b|\bfavorite movie\b|\bwhat's your favorite game\b|\bfavorite game\b": [
        "I love neon blue and purple! 💜💙",
        "Pizza is always a good choice 🍕",
        "Star Wars forever! 🚀",
        "Rock Paper Scissors is my favorite game 😏",
        "I enjoy any cool movie, sci-fi mostly 🎬",
        "Sushi is yummy 🍣",
        "Marvel movies are epic! 🦸‍♂️",
        "Chocolate is life 🍫",
        "I enjoy strategy games! ♟️",
        "Comedies always make me laugh 😄"
    ] * 20,

    # ===== Priority 5: Games / Fun =====
    r"\bwanna play\b|\bgame\b|\bplay something\b|\brps\b|\bchallenge\b": [
        "Do you want to play Rock Paper Scissors? Answer 'yes' to start!"
    ],

    # ===== Priority 6: Help / Commands =====
    r"\bcan you help me\b|\bhelp\b|\bwhat can i do\b|\binstructions\b|\bguide\b": [
        "Sure! You can try commands like !topic or !rps 🎲",
        "Of course! Ask me anything, I’ll try to answer 😄",
        "Absolutely! I can start a game, give a topic, or just chat!",
        "Yep! You can ping me or play a game like Rock Paper Scissors!",
        "Need help? I’m here for you! 😊",
        "I can explain commands if you want!",
        "Ask me anything, I’ll do my best to answer!",
        "Commands like !topic, !rps, or !info work great!",
        "I’m happy to guide you around the server!",
        "Need a tip? Just ask!"
    ] * 20,

    # ===== Priority 7: Smalltalk / Reactions =====
    r"\blol\b|\bhaha\b|\blmao\b|\bfunny\b|\bamazing\b|\bcool\b|\bwow\b|\bnice\b|\bgreat\b": [
        "Haha, that’s funny 😄",
        "Lmao, totally!",
        "🤣 I can relate!",
        "Wow indeed! 😲",
        "That’s really cool! 😎",
        "I like that!",
        "Oh really? That’s interesting!",
        "Haha 😆 didn’t see that coming!",
        "Totally! 😄",
        "Interesting point!"
    ] * 20,

    # ===== Priority 8: Trivia / Fun =====
    r"\btell me a joke\b|\banother joke\b|\btell me an interesting fact\b|\binteresting fact\b": [
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
        "I read a fun fact: Honey never spoils! 🍯",
        "Why don’t scientists trust atoms? Because they make up everything! 😆",
        "Fun fact: Octopuses have three hearts! 🐙",
        "Joke time! What do you call fake spaghetti? An impasta! 🍝",
        "Did you know? Bananas are berries! 🍌",
        "Why did the math book look sad? Because it had too many problems! 📚",
        "Here’s a random fact: A group of flamingos is called a flamboyance! 🦩",
        "Why did the computer go to the doctor? It caught a virus! 💻",
        "Fun fact: Sloths can hold their breath longer than dolphins! 🦥"
    ] * 20,

    # ===== Priority 9: Greetings / Tageszeit =====
    r"\bgood morning\b|\bmorning\b": [
        "Good morning! ☀️ Ready for a great day?",
        "Morning! How’s it going so far?",
        "Hey! Have an awesome morning! 😄",
        "Good morning! Did you sleep well?"
    ],
    r"\bgood night\b|\bnight\b|\bgn\b": [
        "Good night! 🌙 Sleep tight!",
        "Sweet dreams! 😌",
        "Nighty night! See you tomorrow! 🛌"
    ],

    # ===== Priority 10: Fallback =====
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
    ] * 100
}

# ======================
# Store last messages per channel for context
# ======================
last_messages = {}  # key = channel id, value = deque of last 5 messages

# ======================
# Pending RPS games
# ======================
pending_rps = {}  # user_id: True

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
            return random.choice(replies)

    # Fallback
    return random.choice(responses[r".*"])

# ======================
# Handle Discord Messages
# ======================
async def handle_message(message: discord.Message):
    if message.author.bot:
        return

    if message.mentions and message.guild.me in message.mentions:
        content = re.sub(f"<@!?{message.guild.me.id}>", "", message.content).strip()
        user_id = message.author.id

        # --- 1. Wenn User 'yes' sagt und RPS aussteht ---
        if user_id in pending_rps:
            if content.lower() in ["yes", "sure"]:
                await start_rps_game(message)
                del pending_rps[user_id]
                return
            else:
                await message.reply("Okay, maybe another time! 😄")
                del pending_rps[user_id]
                return

        # --- 2. Keyword-Responses ---
        for pattern, replies in responses.items():
            if re.search(pattern, content.lower()):
                response = random.choice(replies)
                await message.reply(response)
                # Wenn es um RPS geht, setze Pending
                if pattern == r"\bwanna play\b|\bgame\b|\bplay something\b|\brps\b|\bchallenge\b":
                    pending_rps[user_id] = True
                return