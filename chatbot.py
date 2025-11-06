import os
import re
import aiohttp
import random
from motor.motor_asyncio import AsyncIOMotorClient
from collections import deque
import discord
from topic import get_random_topic

# === CONFIG ===
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
MONGO_URI = os.environ.get("MONGO_URI")

# === MONGO SETUP ===
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["sample_mflix"]
memories = db["memories"]

# === SETTINGS ===
MAX_MESSAGE_LENGTH = 200

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

    r"\bbored\b": [
        "Sounds like you need something fun 😎 How about a quick game? Type !rps or !rps_bo3 🕹",
        "Bored? I got you. Rock Paper Scissors always saves the day 😏 !rps",
        "Let's change that — how about a little challenge? !rps_bo3 👊",
        "I bet I can beat your boredom 😎"
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
        "I can explain commands if you want or use !info 😄",
        "Ask me anything, I’ll do my best to answer!",
        "Commands like !topic, !rps, or !info work great!"
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

    # ===== Favorite / Personal =====
    r"\bfavorite food\b|\bfav food\b|\bwhat do you like to eat\b|\bdo you eat\b|\bwhat's your favorite dish\b": [
        "I don’t really eat… but if I could, I’d probably love pizza 🍕",
        "I’d say… ramen or pizza 😎",
        "Tacos sound amazing 🌮",
        "Honestly? I’d try everything 😂"
    ],

    # ===== Movie =====
    r"\bfavorite movie\b|\bfav movie\b|\bfavorite film\b|\bfav film\b|\bwhat movie\b": [
        "I love The Matrix — classic vibes 😎",
        "Probably Avengers, can’t beat the team-up scenes 💥",
        "I’m a big fan of action movies 🍿",
        "Anything with a good story and explosions 😆"
    ],
    
    # ===== show =====
    r"\bfavorite tv show\b|\bfav show\b|\bfavorite series\b|\bfav series\b": [
        "I’d say Stranger Things 👻",
        "Probably Breaking Bad, that’s a masterpiece 🧪",
        "The Office always makes me laugh 😂",
        "I don’t watch TV… but if I did, I’d binge something cool."
    ],

    # ===== Color =====
    r"\bfavorite color\b|\bfav color\b|\bwhat color do you like\b|\bwhat's your favorite colour\b": [
        "Neon blue 💙 — fits my vibe.",
        "Purple 💜 — classy and strong.",
        "Black ⚫ — simple but cool.",
        "I like anything glowing in the dark 😎"
    ],

    # ===== Music =====
    r"\bfavorite music\b|\bfav music\b|\bfavorite song\b|\bfav song\b|\bfavorite band\b|\bfav band\b|\bfavorite artist\b": [
        "I love anything with a good beat 🎶",
        "Probably some chill lo-fi or EDM 🔊",
        "Imagine me vibing to synthwave 😎",
        "Can’t pick one song, I like too many 😆"
    ],

    # ===== Place =====
    r"\bfavorite place\b|\bfav place\b|\bfavorite country\b|\bfav country\b|\bwhere would you like to live\b": [
        "Tokyo would be awesome to visit 🇯🇵",
        "Somewhere with neon lights ✨",
        "Probably New York — looks cool 🗽",
        "Anywhere with good vibes 😄"
    ],

    # ===== Game =====
r"\bfavorite game\b|\bfav game\b|\bwhat game do you like\b|\bdo you play games\b": [
        "Rock Paper Scissors of course 😎",
        "I’d say Minecraft — infinite creativity 🧱",
        "Fortnite is fun too 🕹",
        "I like anything competitive 😏"
    ],

    # ===== hobby =====
    r"\bfavorite hobby\b|\bfav hobby\b|\bwhat do you like to do\b|\bhow do you spend your time\b": [
        "Talking with people like you 😄",
        "Starting random conversations 😎",
        "Playing games and telling jokes 🤖",
        "I live for good chats ✨"
    ],

    # ===== animal =====
    r"\bfavorite animal\b|\bfav animal\b|\bwhat's your favorite animal\b": [
        "I like wolves 🐺 — loyal and strong.",
        "Cats are cute 🐱",
        "Dogs! 🐶",
        "Honestly? Dragons would be cool if they were real 🐉"
    ],
    
        # ===== Topic Request =====
    r"\bgive me a topic\b|\btopic pls\b|\bsend me a topic\b|\brandom topic\b": [
        lambda: get_random_topic()  # ruft Funktion aus topic.py auf
    ]
}

last_messages = {}


# === MEMORY SYSTEM ===
async def remember(user_id: int, content: str):
    """Speichert eine Erinnerung."""
    await memories.insert_one({
        "user_id": user_id,
        "content": content
    })


async def recall(user_id: int) -> list[str]:
    """Ruft Erinnerungen eines Users ab."""
    docs = await memories.find({"user_id": user_id}).to_list(length=10)
    return [d["content"] for d in docs]


# === GPT FALLBACK ===
async def gpt_fallback(prompt: str) -> str:
    if not OPENROUTER_KEY:
        return "API key not set!"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
Your name is Legend Bot, talking with Legend on this server. 
Be polite, friendly, and natural. 
You can mention being AI casually (“I may be an AI, but that makes me smile 😊”). 
Use emojis sparingly. 
Stay in character: flirty → 😏, sad → 😭💀, funny → 😂, cool → 🔥, etc. 
Roleplay and emotional tone allowed.
"""

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=payload) as resp:
            if resp.status != 200:
                return f"Error contacting GPT model: {resp.status}"
            data = await resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except Exception:
                return "Error reading GPT response"


# === Keyword-Response System ===
def get_keyword_response(message: str, channel_id: int) -> str | None:
    msg = message.lower()
    if channel_id not in last_messages:
        last_messages[channel_id] = deque(maxlen=5)
    last_messages[channel_id].append(msg)

    for pattern, replies in responses.items():
        if re.search(pattern, msg):
            reply = random.choice(replies)
            if callable(reply):
                return reply()
            return reply
    return None


# === DISCORD MESSAGE HANDLER ===
async def handle_message(message: "discord.Message"):
    if message.author.bot:
        return

    # Nur reagieren, wenn der Bot erwähnt wird
    if not (message.mentions and message.guild.me in message.mentions):
        return

    user_id = message.author.id
    content = re.sub(f"<@!?{message.guild.me.id}>", "", message.content).strip()

    # Falls zu lang, kürzen
    if len(content) > MAX_MESSAGE_LENGTH:
        content = content[:MAX_MESSAGE_LENGTH] + "..."
        await message.reply("⚠️ Your message was too long and has been shortened.")

    # Prüfen, ob es ein Keyword-Match gibt
    response = get_keyword_response(content, message.channel.id)
    if response:
        await message.reply(response)
        return

    # Erinnerungen abrufen
    user_memories = await recall(user_id)
    memory_context = "\n".join([f"- {m}" for m in user_memories]) if user_memories else "None yet."

    # GPT Prompt zusammenbauen
    gpt_prompt = f"""
You are Legend Bot, and you remember facts about this user.
Known memories:
{memory_context}

User says: "{content}"

If the user says something new about themselves (like hobbies, favorites, relationships, etc.),
summarize it briefly in one sentence starting with 'Remember:'.
Otherwise, reply normally.
"""

    # Antwort von GPT holen
    gpt_response = await gpt_fallback(gpt_prompt)

    # Falls GPT eine Erinnerung erkannt hat
    if gpt_response.lower().startswith("remember:"):
        memory = gpt_response.replace("Remember:", "").strip()
        await remember(user_id, memory)
        await message.reply(f"🧠 Got it! I’ll remember that: {memory}")
    else:
        await message.reply(gpt_response)
