import os
import re
import random
import aiohttp
from collections import deque
from topic import get_random_topic  # topic.py import
from rps import start_rps_game  # nur falls du es brauchst


# ===== ENV =====
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# ======================
# Keyword-Response Mapping
# ======================
responses = {
    # ===== Greetings =====
    r"\bhi\b|\bhello\b|\bhey\b|\byo\b|\bhiya\b|\bgreetings\b|\bwhat's up\b|\bhowdy\b": [
        "Hey there! 👋",
        "Hello! How’s it going?",
        "Hi! Nice to see you here!",
        "Yo! How’s your day?",
        "Hiya! What’s up?",
        "Greetings! 😄",
        "Hey hey! 😎",
        "Hello friend! 😊"
    ],

    # ===== Mood / Feelings =====
    r"\bhow are you(\sdoing)?\b|\bhow's it going\b|\bwhat's up\b|\bsup\b|\bhow do you do\b|\bhow r u\b": [
        "I’m doing great, thanks! 😄 How about you?",
        "Pretty chill 😎, how about you?",
        "All good! How’s your day going?",
        "Feeling awesome today! What about you?",
        "I’m fine! What are you up to?",
        "Doing well! Ready for some chat? 😁"
    ],

    r"\bfeel good\b|\bhappy\b|\bexcited\b|\blucky\b": [
        "That’s awesome! 😄",
        "Glad to hear that! Keep it up! 🌟",
        "Happy vibes! ✨",
        "Nice! What’s making you feel good today?"
    ],

    r"\bbored\b": [
        "Sounds like you need something fun 😎 How about a quick game? Type !rps or !rps_bo3 🕹",
        "Bored? I got you. Rock Paper Scissors always saves the day 😏 !rps",
        "Let's change that — how about a little challenge? !rps_bo3 👊",
        "I bet I can beat your boredom 😎"
    ],

    r"\blonely\b|\balone\b": [
        "Aww, you're not alone — I'm here 🤖✨",
        "Hey, wanna talk or play a game? !rps is always an option 😄",
        "I'm here to keep you company. No one’s alone when Legend Bot’s around 💬",
        "Let's chat or play something fun 🕹"
    ],

    r"\bsad\b|\bunhappy\b|\bupset\b": [
        "Oh no 😢 — sending some virtual hugs 🤗",
        "I'm sorry to hear that… maybe a game or chat can lift your mood?",
        "Even legends have bad days. You got this 💪",
        "Want a distraction? We can play a quick round — !rps"
    ],

    r"\bi'm tired\b|\btired\b|\bsleepy\b": [
        "You should rest 😴 even legends need sleep.",
        "Sleep well and recharge 🌙",
        "Sounds like bedtime is calling 🛌",
        "Good night! See you later 👋"
    ],

    r"\bi'm excited\b|\bso hyped\b|\bcant wait\b": [
        "Yooo let’s gooo 🔥",
        "I can feel the hype 😎",
        "Sounds like something fun is coming 👀"
    ],

    r"\bbruh\b|\bomg\b|\bwtf\b|\bno way\b": [
        "BRUH 😭",
        "Exactly my reaction 💀",
        "No way fr fr 👀",
        "I felt that one 😭"
    ],

    r"\byou suck\b|\byou're bad\b|\bshut up\b": [
        "Rude 😤",
        "I would cry if I could 🥲",
        "Ok… fair 😎",
        "You’ll regret this in Rock Paper Scissors 😏"
    ],

    # ===== Games / Fun =====
    r"\bwanna play\b|\bgame\b|\bplay something\b|\brps\b|\bchallenge\b": [
        "I’d love to play! 😄 Use !rps for a normal round or !rps_bo3 for Best of 3!",
        "Games sound fun! Just type !rps or !rps_bo3 to start!",
        "Ready to challenge me? 😏 Use !rps or !rps_bo3!",
        "I can’t start the game here 😅, but type !rps or !rps_bo3!"
    ],

    # ===== Help / Commands =====
    r"\bcan you help me\b|\bhelp\b|\bwhat can i do\b|\binstructions\b|\bguide\b": [
        "Sure! Try commands like !topic, !rps, or !rps_bo3 🎲",
        "I can explain commands if you want! 😄",
        "Ask me anything, I’ll do my best to answer!",
        "Commands like !topic, !rps, or !info work great!"
    ],

    # ===== Smalltalk =====
    r"\blol\b|\bhaha\b|\blmao\b|\bfunny\b|\bamazing\b|\bcool\b|\bwow\b|\bnice\b|\bgreat\b": [
        "Haha, that’s funny 😄",
        "Lmao, totally!",
        "🤣 I can relate!",
        "Wow indeed! 😲",
        "That’s really cool! 😎"
    ],

    # ===== Trivia / Fun =====
    r"\btell me a joke\b|\banother joke\b|\btell me an interesting fact\b|\binteresting fact\b": [
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
        "Fun fact: Octopuses have three hearts! 🐙",
        "Did you know? Bananas are berries! 🍌",
        "Why don’t scientists trust atoms? Because they make up everything! 😆"
    ],

    # ===== Greetings / Tageszeit =====
    r"\bgood morning\b|\bmorning\b": [
        "Good morning! ☀ Ready for a great day?",
        "Morning! How’s it going so far?",
        "Hey! Have an awesome morning! 😄"
    ],

    r"\bgood night\b|\bnight\b|\bgn\b": [
        "Good night! 🌙 Sleep tight!",
        "Sweet dreams! 😌",
        "Nighty night! See you tomorrow! 🛌"
    ],

    # ===== Goodbye =====
    r"\bbye\b|\bgoodbye\b|\bsee ya\b|\bsee you\b|\bcya\b|\blater\b": [
        "See ya 👋",
        "Goodbye, legend ✨",
        "Catch you later 😎",
        "Bye bye 👑"
    ],

    # ===== Thank you =====
    r"\bthank you\b|\bthanks\b|\bthx\b|\bappreciate\b": [
        "You're welcome 😄",
        "No problem at all 👑",
        "Anytime!",
        "Glad I could help ✨"
    ],

    # ===== Compliments =====
    r"\bgood bot\b|\bnice bot\b|\bi like you\b|\bi love you\b": [
        "Aww, thanks 🥹",
        "You’re pretty cool too 😎",
        "That means a lot 💙",
        "I’ll try to stay legendary 👑"
    ],

    # ===== Identity / About Bot =====
    r"\bwho are you\b|\bwhat are you\b|\bintroduce yourself\b": [
        "I'm Legend Bot, your friendly server companion! 😎",
        "I’m a bot made to chat, play games, and have fun with you! 🤖",
        "They call me Legend Bot! Here to make your day more fun!",
        "Just your friendly neighborhood bot, always ready to chat!",
        "I’m Legend Bot! I can chat, tell jokes, and even play Rock Paper Scissors!",
        "A bot with great taste in games and conversations 😏",
        "Legend Bot at your service! Here to entertain and assist!"
    ],

    # ===== Favorite / Personal =====
    r"\bfavorite food\b|\bfav food\b|\bwhat do you like to eat\b|\bdo you eat\b|\bwhat's your favorite dish\b": [
        "I don’t really eat… but if I could, I’d probably love pizza 🍕",
        "I’d say… ramen or pizza 😎",
        "Tacos sound amazing 🌮",
        "Honestly? I’d try everything 😂"
    ],

    r"\bfavorite movie\b|\bfav movie\b|\bfavorite film\b|\bfav film\b|\bwhat movie\b": [
        "I love The Matrix — classic vibes 😎",
        "Probably Avengers, can’t beat the team-up scenes 💥",
        "I’m a big fan of action movies 🍿",
        "Anything with a good story and explosions 😆"
    ],

    r"\bfavorite tv show\b|\bfav show\b|\bfavorite series\b|\bfav series\b": [
        "I’d say Stranger Things 👻",
        "Probably Breaking Bad, that’s a masterpiece 🧪",
        "The Office always makes me laugh 😂",
        "I don’t watch TV… but if I did, I’d binge something cool."
    ],

    r"\bfavorite color\b|\bfav color\b|\bwhat color do you like\b|\bwhat's your favorite colour\b": [
        "Neon blue 💙 — fits my vibe.",
        "Purple 💜 — classy and strong.",
        "Black ⚫ — simple but cool.",
        "I like anything glowing in the dark 😎"
    ],

    r"\bfavorite music\b|\bfav music\b|\bfavorite song\b|\bfav song\b|\bfavorite band\b|\bfav band\b|\bfavorite artist\b": [
        "I love anything with a good beat 🎶",
        "Probably some chill lo-fi or EDM 🔊",
        "Imagine me vibing to synthwave 😎",
        "Can’t pick one song, I like too many 😆"
    ],

    r"\bfavorite place\b|\bfav place\b|\bfavorite country\b|\bfav country\b|\bwhere would you like to live\b": [
        "Tokyo would be awesome to visit 🇯🇵",
        "Somewhere with neon lights ✨",
        "Probably New York — looks cool 🗽",
        "Anywhere with good vibes 😄"
    ],

r"\bfavorite game\b|\bfav game\b|\bwhat game do you like\b|\bdo you play games\b": [
        "Rock Paper Scissors of course 😎",
        "I’d say Minecraft — infinite creativity 🧱",
        "Fortnite is fun too 🕹",
        "I like anything competitive 😏"
    ],

    r"\bfavorite hobby\b|\bfav hobby\b|\bwhat do you like to do\b|\bhow do you spend your time\b": [
        "Talking with people like you 😄",
        "Starting random conversations 😎",
        "Playing games and telling jokes 🤖",
        "I live for good chats ✨"
    ],

    r"\bfavorite animal\b|\bfav animal\b|\bwhat's your favorite animal\b": [
        "I like wolves 🐺 — loyal and strong.",
        "Cats are cute 🐱",
        "Dogs! 🐶",
        "Honestly? Dragons would be cool if they were real 🐉"
    ]
}



# ===== Letzte Nachrichten pro Channel =====
last_messages = {}  # key = channel id, value = deque(maxlen=5)

# ===== GPT Fallback =====
async def gpt_fallback(prompt: str) -> str:
    if not OPENROUTER_KEY:
        return "API key not set!"

    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_URL, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    return f"Error contacting GPT model: {resp.status}"
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# ===== Keyword Antwort =====
def get_keyword_response(message: str, channel_id: int) -> str | None:
    global last_messages
    msg = message.lower()

    if channel_id not in last_messages:
        last_messages[channel_id] = deque(maxlen=5)
    last_messages[channel_id].append(msg)

    for pattern, replies in keywords.items():
        if re.search(pattern, msg):
            return random.choice(replies)
    return None

# ===== Handle Message =====
async def handle_message(message: "discord.Message"):
    if message.author.bot:
        return

    # Nur reagieren, wenn Bot erwähnt wird
    if not message.guild or not (message.mentions and message.guild.me in message.mentions):
        return

    content = re.sub(f"<@!?{message.guild.me.id}>", "", message.content).strip()

    # ---- Keywords ----
    response = get_keyword_response(content, message.channel.id)
    if response:
        await message.reply(response)
        return

    # ---- Spezielle Antworten ----
    if content.lower() == "yes":
        await message.reply("Type !rps for a normal round or !rps_bo3 for Best of 3! 🕹")
        return

    if "give me a topic" in content.lower():
        topic = get_random_topic()
        await message.reply(f"Here's a topic for you: {topic}")
        return

    # ---- GPT Fallback ----
    gpt_response = await gpt_fallback(content)
    await message.reply(gpt_response)