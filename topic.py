import random
from datetime import datetime, timedelta
import pytz
from discord.ext import tasks

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

class ChatReviver:
    def __init__(self, bot, channel_id, inactivity_hours=2, night_start=22, night_end=8, timezone="Europe/Berlin"):
        self.bot = bot
        self.channel_id = channel_id
        self.inactivity_hours = inactivity_hours
        self.night_start = night_start
        self.night_end = night_end
        self.timezone = timezone
        self.last_activity = datetime.now(pytz.timezone(self.timezone))

    @tasks.loop(minutes=10)
    async def check_inactivity(self):
        now = datetime.now(pytz.timezone(self.timezone))
        hour = now.hour

        # Night mode
        if self.night_start <= hour or hour < self.night_end:
            return

        if (now - self.last_activity) > timedelta(hours=self.inactivity_hours):
            channel = self.bot.get_channel(self.channel_id)
            if channel:
                await channel.send(f"@chat revive, here's a question: {get_random_topic()}")

    def update_activity(self):
        self.last_activity = datetime.now(pytz.timezone(self.timezone))

    async def start(self):
        self.check_inactivity.start()