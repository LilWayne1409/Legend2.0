import random
from datetime import datetime, timedelta
import pytz
import asyncio
from discord.ext import tasks

# ========================
# 📜 Fragenliste
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

        if (now - self.last_activity) > timedelta(hours=self.inactivity_hours):
            if not self.last_ping or (now - self.last_ping) > timedelta(hours=self.inactivity_hours):
                await self.send_deadchat_ping()
                self.last_ping = now

    async def send_deadchat_ping(self):
        channel = self.bot.get_channel(self.revive_channel_id)
        if channel:
            DEADCHAT_ROLE_ID = 1422570834836455585  # Deadchat Ping Rolle
            UNDEAD_ROLE_ID = 1430557660478177331     # 👑 Die Rolle, die der nächste Schreiber bekommt (ändern!)
            deadchat_role = channel.guild.get_role(DEADCHAT_ROLE_ID)
            undead_role = channel.guild.get_role(UNDEAD_ROLE_ID)

            question = get_random_topic()

            # 📨 Nachricht mit Ping und Hinweis auf Rolle
            if deadchat_role and undead_role:
                await channel.send(
                    f"{deadchat_role.mention} 👀 The chat looks pretty quiet...\n"
                    f"💬 Here's a topic: **{question}**\n"
                    f"⚡ The **first person** to answer will get the {undead_role.mention} role!"
                )
            elif deadchat_role:
                await channel.send(
                    f"{deadchat_role.mention} 👀 The chat looks pretty quiet...\n"
                    f"💬 Here's a topic: **{question}**"
                )
            else:
                await channel.send(
                    f"👀 The chat looks pretty quiet...\n💬 Here's a topic: **{question}**"
                )

            def check(msg):
                return msg.channel.id == channel.id and not msg.author.bot

            try:
                # ⏳ 120 Sek warten auf Antwort
                msg = await self.bot.wait_for("message", check=check, timeout=120.0)

                if undead_role:
                    await msg.author.add_roles(undead_role, reason="First to revive chat")
                    await channel.send(f"👑 {msg.author.mention} has been crowned as {undead_role.mention}!")

            except asyncio.TimeoutError:
                await channel.send("⏳ Nobody answered in time… maybe next time 👻")

    async def trigger_revive(self):
        """Manuell triggern mit !revive"""
        await self.send_deadchat_ping()

    def update_activity(self):
        self.last_activity = datetime.now(pytz.timezone(self.timezone))

    async def start(self):
        self.check_inactivity.start()