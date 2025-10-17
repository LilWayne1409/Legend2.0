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
    embed.set_footer(text="Legend Bot • Keeps Legends Active 👑")
    await ctx.send(embed=embed)

# ==== RUN BOT ====
bot.run(TOKEN)