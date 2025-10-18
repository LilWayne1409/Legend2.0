import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from rps import RPSView, RPSBo3View
from topic import get_random_topic
from chatbot import handle_message  # dein Keyword-Responder

# ==== ENV ====
load_dotenv()
TOKEN = os.environ.get("TOKEN")

# ==== INTENTS ====
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- Welcome Messages with Bot Intro ----
welcome_messages = [
    "Hey {member}, welcome to Lagged Legends! 🎮 I’m Legend Bot 🤖, your AI companion. Try mentioning me to start a chat!",
    "Welcome, {member}! 👑 I’m Legend Bot, here to keep the server legendary. Want a topic to talk about? Just ask me!",
    "Yo {member}! 😎 Legend Bot here — I can chat, play mini-games, or give you fun topics. Say hi and see what happens!",
    "Glad you joined, {member}! 💬 I’m Legend Bot, your AI buddy. Mention me anytime to start a conversation!",
    "Welcome to Lagged Legends, {member}! 🕹 I’m Legend Bot 🤖. I love chatting and sharing random topics — give me a try!",
    "Hey hey {member}! 🌟 Legend Bot here. You can talk to me, play !rps, or ask me for a topic. Let’s make it fun!",
    "Hello {member}! 🤖 I’m Legend Bot, your new AI companion. Want to start chatting? Just mention me and say something!",
    "Welcome aboard, {member}! 🚀 I’m Legend Bot. I can answer questions, give topics, and even play mini-games with you!",
    "What’s up {member}? 😄 I’m Legend Bot, ready to spice up the chat. Mention me and start a conversation!",
    "Greetings {member}! ✨ Legend Bot here — chat with me, get random topics, or challenge me to a game. Let’s go!"
]

# ---- Event: Member Join ----
@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(CHANNEL_ID)  # Set your welcome channel ID
    if channel:
        message = random.choice(welcome_messages).format(member=member.mention)
        await channel.send(message)
        
# ==== EVENTS ====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="!info"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Prüfen, ob es ein Command ist
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
        return  # Wichtig: KEIN handle_message bei Commands

    # Keyword-Responder reagiert nur auf Nachrichten ohne Command
    await handle_message(message)

# ==== COMMANDS ====
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 {round(bot.latency * 1000)}ms")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hey {ctx.author.mention}! 👋")

@bot.command()
async def topic(ctx):
    await ctx.send(f"💬 Random Topic:\n{get_random_topic()}")

@bot.command()
async def rps(ctx, opponent: discord.Member = None):
    embed = discord.Embed(
        title="Rock Paper Scissors",
        description="Choose one:",
        color=0x00ff00
    )
    view = RPSView(ctx, opponent)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def rps_bo3(ctx, opponent: discord.Member = None):
    embed = discord.Embed(
        title="Rock Paper Scissors - Best of 3",
        description="Choose one:",
        color=0x00ff00
    )
    view = RPSBo3View(ctx, opponent)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="🤖 Legend Bot Info",
        description="I'm Legend Bot, keeping your server active and fun! 👑",
        color=discord.Color.blurple()
    )
    embed.add_field(
        name="Commands",
        value=(
            "**!ping** - Check latency\n"
            "**!hello** - Say hi to the bot\n"
            "**!topic** - Get a random chat topic\n"
            "**!rps [@User]** - Play Rock Paper Scissors\n"
            "**!rps_bo3 [@User]** - Play Best of 3 Rock Paper Scissors\n"
            "**!info** - Show this info message"
        ),
        inline=False
    )
    embed.add_field(
        name="Other Features",
        value=(
            "- Responds **only when mentioned** (@Legend Bot)\n"
            "- Keyword responses for greetings, moods, games, fun, etc.\n"
            "- Multiple ways to ask for a topic (e.g., 'give me a topic', 'random topic')\n"
            "- GPT fallback if your message doesn't match any keyword\n"
            "- Auto-truncates messages longer than 200 characters"
        ),
        inline=False
    )
    embed.set_footer(text="Legend Bot • Keeps Legends Active 👑")
    await ctx.send(embed=embed)

# ==== RUN BOT ====
bot.run(TOKEN)