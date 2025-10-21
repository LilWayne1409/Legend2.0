import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from rps import RPSView, RPSBo3View
from topic import get_random_topic
from chatbot import handle_message
from topic import ChatReviver
# ==== ENV ====
load_dotenv()
TOKEN = os.environ.get("TOKEN")

# ==== CONFIG ====
CHANNEL_ID = 1419352213607809046  
REVIVE_CHANNEL_ID = 1419352213607809046 
WELCOME_CHANNEL_ID = 1419352213607809046

# ==== INTENTS ====
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True  # 👈 wichtig für on_member_join

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- Welcome Messages ----
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

# ---- Initialize Chat Reviver ----
chat_reviver = ChatReviver(bot, REVIVE_CHANNEL_ID)

# ---- Event: Member Join ----
@bot.event
async def on_member_join(member):
    print(f"🎉 New member joined: {member.name}")
    channel = member.guild.get_channel(CHANNEL_ID)
    if channel:
        message = random.choice(welcome_messages).format(member=member.mention)
        await channel.send(message)
    else:
        print("❌ Could not find the welcome channel!")

# ---- Test command for debugging ----
@bot.command()
async def test_join(ctx):
    channel = ctx.guild.get_channel(CHANNEL_ID)
    if channel:
        await ctx.send(f"✅ Found channel: {channel.name}")
        await channel.send(f"Simulated join for {ctx.author.mention} 🎉")
    else:
        await ctx.send("❌ Channel not found!")
        
# ==== EVENTS ====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="!info"))
    await chat_reviver.start()  # <<< Deadchat-Loop starten

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Aktivität aktualisieren für ChatReviver
    chat_reviver.update_activity()

    # Prüfen, ob es ein Command ist
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
        return

    await handle_message(message)

# ==== COMMANDS ====
@bot.command()
async def revive(ctx):
    """Manually trigger Deadchat for Admins, Staff, and Prestige roles."""
    allowed_roles = ["-----------------Staff-------------------", "Legend"]
    author_roles = [role.name for role in ctx.author.roles]

    if not any(role in allowed_roles for role in author_roles):
        await ctx.send("❌ You don't have permission to use this command!")
        return

    # Trigger Deadchat (optional, z. B. Logik aus ChatReviver)
    await chat_reviver.trigger_revive()

    # Deadchat Ping
    DEADCHAT_ROLE_ID = 1422570834836455585  # <- deine Role ID
    revive_channel = ctx.guild.get_channel(REVIVE_CHANNEL_ID)
    if revive_channel:
        role = ctx.guild.get_role(DEADCHAT_ROLE_ID)
        question = get_random_topic()
        if role:
            await revive_channel.send(
                f"{role.mention} 👀 The chat looks pretty quiet... here's a topic: {question}"
            )
        else:
            await revive_channel.send(
                f"👀 The chat looks pretty quiet... here's a topic: {question}"
            )
    
@bot.command()
async def test_welcome(ctx):
    member = ctx.author
    channel = ctx.guild.get_channel(CHANNEL_ID)
    await channel.send(random.choice(welcome_messages).format(member=member.mention))
    
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
            "- Auto-truncates messages longer than 200 characters\n"
            "- **Deadchat System**: Revives the chat automatically after inactivity 👀"
        ),
        inline=False
    )
    embed.set_footer(text="Legend Bot • Keeps Legends Active 👑")
    await ctx.send(embed=embed)

# ==== RUN BOT ====
bot.run(TOKEN)
