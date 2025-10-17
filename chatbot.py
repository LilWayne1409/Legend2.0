import random
import re
import discord

# ===== Keyword-Responses Mapping =====
responses = {
    # Casual greetings and small talk
    "hi|hello|hey|what's up|how's it going|good morning|good night": [
        "Hey there! How’s everything going today?",
        "Haha, that’s actually funny 😄",
        "I totally get what you mean.",
        "That’s a good question… let me think 🤔",
        "Interesting point — never thought about it like that.",
        "Yeah, it’s been a long day for me too.",
        "What are you up to right now?",
        "I like how you put that!",
        "Tell me more about that.",
        "Same here, honestly.",
        "That’s kinda true tho 😂",
        "Oh really? That’s cool!",
        "Do you play any games lately?",
        "I feel that 😅",
        "What’s your favorite movie or show?",
        "That reminds me of something funny actually.",
        "Lmao yeah that happens a lot",
        "What time is it for you right now?",
        "Do you usually stay up late?",
        "That’s awesome!",
        "You’re actually right about that.",
        "I didn’t expect that answer 😄",
        "Wait, really??",
        "I can relate to that for real.",
        "Good vibe right there!",
        "Let’s gooo 🔥",
        "What’s your plan for the weekend?",
        "That’s a nice thing to say, thanks!",
        "I was thinking about the same thing tbh.",
        "That’s the energy we need 😎",
        "Oof yeah that’s rough 😬",
        "Good morning ☀️ or maybe good night?",
        "Haha classic!",
        "That’s a solid take actually.",
        "Not gonna lie, that sounds fun.",
        "You’ve got a point there!",
        "That’s fair.",
        "I see where you’re coming from.",
        "Okay that’s actually interesting 👀",
        "True true 😌"
    ]
}

# ===== Function to get response =====
def get_response(message: str) -> str:
    msg = message.lower()
    for keyword_pattern, reply_list in responses.items():
        # Prüft alle Varianten (getrennt durch "|")
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