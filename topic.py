import random
from datetime import datetime, timedelta
import pytz
from discord.ext import tasks

# ========================
# 📜 Liste der Fragen
# ========================
questions = [
    "What's your favorite game?", "What's your dream vacation?", "If you could have any superpower, what would it be?",
    "What's your favorite movie?", "What's a skill you want to learn?", "What's your favorite book?",
    "What's your favorite food?", "If you could live anywhere, where would it be?", "What's your favorite hobby?",
    "What's a talent you have?", "What's your favorite song?", "What's your favorite TV show?",
    "What's your favorite animal?", "If you could meet anyone, dead or alive, who would it be?", "What's your favorite color?",
    "What's your favorite sport?", "What's your favorite season?", "Do you prefer cats or dogs?",
    "What's a fun fact about you?", "What's your favorite holiday?", "What's your favorite childhood memory?",
    "What's your favorite drink?", "Do you prefer mountains or the beach?", "What's your favorite dessert?",
    "What's your favorite app?", "What's a country you want to visit?", "What's your favorite quote?",
    "What's your favorite board game?", "Do you prefer morning or night?", "What's your favorite type of music?",
    "What's your guilty pleasure?", "What's a habit you're proud of?", "What's your favorite fruit?",
    "What's your favorite vegetable?", "What's your favorite superhero?", "What's your favorite video game?",
    "What's your dream job?", "Do you prefer coffee or tea?", "What's your favorite restaurant?",
    "What's your favorite way to relax?", "What's your favorite city?", "What's your favorite holiday destination?",
    "What's your favorite ice cream flavor?", "What's your favorite TV character?", "What's your favorite childhood toy?",
    "What's your favorite season of the year?", "What's your favorite candy?", "What's your favorite clothing brand?",
    "What's your favorite flower?", "What's your favorite kind of weather?", "What's your favorite social media platform?"
]

def get_random_topic():
    return random.choice(questions)


# ========================
# ⚡ Chat Reviver Klasse
# ========================
class ChatReviver:
    def __init__(self, bot, revive_channel_id, inactivity_hours=1.5, night_start=22, night_end=8, timezone="Europe/Berlin"):
        self.bot = bot
        self.revive_channel_id = revive_channel_id
        self.inactivity_hours = inactivity_hours
        self.night_start = night_start
        self.night_end = night_end
        self.timezone = timezone
        self.last_activity = datetime.now(pytz.timezone(self.timezone))
        self.last_ping = None

    @tasks.loop(minutes=10)
    async def check_inactivity(self):
        now = datetime.now(pytz.timezone(self.timezone))
        hour = now.hour

        # 🌙 Nachtmodus aktiv
        if self.night_start <= hour or hour < self.night_end:
            return

        # ⏳ Inaktivität prüfen
        if (now - self.last_activity) > timedelta(hours=self.inactivity_hours):
            if not self.last_ping or (now - self.last_ping) > timedelta(hours=self.inactivity_hours):
                channel = self.bot.get_channel(self.revive_channel_id)
                if channel:
                    role = next((r for r in channel.guild.roles if r.name.lower() == "chat revive"), None)
                    if role:
                        await channel.send(f"{role.mention}, here's a question: {get_random_topic()}")
                    else:
                        await channel.send(f"@chat revive (role not found), here's a question: {get_random_topic()}")
                self.last_ping = now

    # ---- NEUE METHODE für manuellen Trigger ----
    async def trigger_revive(self):
        """Post a deadchat question immediately, ignoring inactivity and night mode."""
        channel = self.bot.get_channel(self.revive_channel_id)
        if channel:
            role = next((r for r in channel.guild.roles if r.name.lower() == "chat revive"), None)
            question = get_random_topic()
            if role:
                await channel.send(f"{role.mention}, here's a question: {question}")
            else:
                await channel.send(f"Here's a question: {question}")
            self.last_ping = datetime.now(pytz.timezone(self.timezone))

    def update_activity(self):
        self.last_activity = datetime.now(pytz.timezone(self.timezone))

    async def start(self):
        self.check_inactivity.start()