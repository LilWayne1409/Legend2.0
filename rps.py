import random
import discord
from discord.ui import View, Button

CHOICES = {
    "Rock": "🪨",
    "Paper": "📄",
    "Scissors": "✂️"
}

# =====================
# --- Single Round ---
# =====================
class RPSView(View):
    def __init__(self, ctx, opponent: discord.Member = None, timeout=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.player1 = ctx.author
        self.player2 = opponent or ctx.bot.user
        self.choices = {}
        for choice in CHOICES:
            self.add_item(RPSButton(choice, self))

    async def end_round_if_ready(self):
        if len(self.choices) == 2:
            p1_choice = self.choices[self.player1]
            p2_choice = self.choices[self.player2]
            wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}

            if p1_choice == p2_choice:
                result = "It's a tie!"
            elif wins[p1_choice] == p2_choice:
                result = f"{self.player1.mention} wins!"
            else:
                result = f"{self.player2.mention if self.player2 != self.ctx.bot.user else 'Bot'} wins!"

            embed = discord.Embed(
                title="🕹️ Rock Paper Scissors",
                description=(
                    f"{self.player1.mention} chose **{p1_choice}** {CHOICES[p1_choice]}\n"
                    f"{self.player2.mention if self.player2 != self.ctx.bot.user else 'Bot'} chose **{p2_choice}** {CHOICES[p2_choice]}\n\n"
                    f"**{result}**"
                ),
                color=discord.Color.blurple()
            )
            await self.ctx.channel.send(embed=embed)
            self.stop()


class RPSButton(Button):
    def __init__(self, label, parent_view):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user

        if user not in [self.parent_view.player1, self.parent_view.player2]:
            await interaction.response.send_message("❌ You're not part of this game!", ephemeral=True)
            return

        if user in self.parent_view.choices:
            await interaction.response.send_message("⚠️ You already made your choice!", ephemeral=True)
            return

        self.parent_view.choices[user] = self.label
        await interaction.response.send_message(f"You chose **{self.label}** {CHOICES[self.label]}", ephemeral=True)

        if self.parent_view.player2 == self.parent_view.ctx.bot.user and len(self.parent_view.choices) == 1:
            bot_choice = random.choice(list(CHOICES.keys()))
            self.parent_view.choices[self.parent_view.player2] = bot_choice

        await self.parent_view.end_round_if_ready()


# =====================
# --- Best of 3 Mode ---
# =====================
class RPSBo3View(View):
    def __init__(self, ctx, opponent: discord.Member = None, timeout=90):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.player1 = ctx.author
        self.player2 = opponent or ctx.bot.user
        self.scores = {self.player1: 0, self.player2: 0}
        self.round = 1
        self.choices = {}
        self.message = None  # Speichert die Embed-Nachricht
        for choice in CHOICES:
            self.add_item(RPSBo3Button(choice, self))

    async def start_game(self):
        desc = f"{self.player1.mention} started **Best of 3 Rock Paper Scissors!**\n"
        if self.player2 != self.ctx.bot.user:
            desc += f"Opponent: {self.player2.mention}\nFirst to 2 wins 🏆\nMake your choice 👇"
        else:
            desc += "You're playing against the Bot 🤖\nFirst to 2 wins 🏆\nMake your choice 👇"

        embed = discord.Embed(
            title="🪨📄✂️ Rock Paper Scissors - Best of 3",
            description=desc,
            color=discord.Color.blurple()
        )
        self.message = await self.ctx.send(embed=embed, view=self)

    async def play_round(self):
        if len(self.choices) == 2:
            p1_choice = self.choices[self.player1]
            p2_choice = self.choices[self.player2]
            wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}

            if p1_choice == p2_choice:
                result = "It's a tie!"
            elif wins[p1_choice] == p2_choice:
                result = f"{self.player1.mention} wins this round!"
                self.scores[self.player1] += 1
            else:
                result = f"{self.player2.mention if self.player2 != self.ctx.bot.user else 'Bot'} wins this round!"
                self.scores[self.player2] += 1

            # Update Embed
            embed = discord.Embed(
                title=f"Round {self.round}",
                description=(
                    f"{self.player1.mention} chose **{p1_choice}** {CHOICES[p1_choice]}\n"
                    f"{self.player2.mention if self.player2 != self.ctx.bot.user else 'Bot'} chose **{p2_choice}** {CHOICES[p2_choice]}\n\n"
                    f"**{result}**\n\n"
                    f"🏁 Score: {self.scores[self.player1]} - {self.scores[self.player2]}"
                ),
                color=discord.Color.blurple()
            )

            # Check for final winner
            if self.scores[self.player1] == 2 or self.scores[self.player2] == 2:
                winner = self.player1 if self.scores[self.player1] > self.scores[self.player2] else self.player2
                winner_text = winner.mention if winner != self.ctx.bot.user else "Bot"
                embed.title = "🏆 Final Result"
                embed.description += f"\n\n{winner_text} wins the Best of 3 match!"
                await self.message.edit(embed=embed, view=None)  # Buttons entfernen
                self.stop()
            else:
                self.round += 1
                self.choices = {}
                await self.message.edit(embed=embed)  # Embed aktualisieren

class RPSBo3Button(Button):
    def __init__(self, label, parent_view):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user

        if user not in [self.parent_view.player1, self.parent_view.player2]:
            await interaction.response.send_message("❌ You're not part of this game!", ephemeral=True)
            return

        if user in self.parent_view.choices:
            await interaction.response.send_message("⚠️ You already made your choice!", ephemeral=True)
            return

        # Choice speichern und Buttons kurz deaktivieren
        self.parent_view.choices[user] = self.label
        for item in self.parent_view.children:
            item.disabled = True
        await self.parent_view.message.edit(view=self.parent_view)

        await interaction.response.send_message(f"You chose **{self.label}** {CHOICES[self.label]}", ephemeral=True)

        # Bot Choice, falls kein Gegner
        if self.parent_view.player2 == self.parent_view.ctx.bot.user and len(self.parent_view.choices) == 1:
            bot_choice = random.choice(list(CHOICES.keys()))
            self.parent_view.choices[self.parent_view.player2] = bot_choice

        # Buttons wieder aktivieren für nächste Runde
        for item in self.parent_view.children:
            item.disabled = False
        await self.parent_view.play_round()


# =====================
# --- Commands ---
# =====================
async def start_rps_game(ctx, opponent: discord.Member = None):
    view = RPSView(ctx, opponent)
    desc = f"{ctx.author.mention} started Rock Paper Scissors!\n"
    if opponent:
        desc += f"Opponent: {opponent.mention}\nBoth players make your choice 👇"
    else:
        desc += "You're playing against the Bot 🤖\nMake your choice below 👇"

    embed = discord.Embed(title="🪨📄✂️ Rock Paper Scissors", description=desc, color=discord.Color.blurple())
    await ctx.send(embed=embed, view=view)


async def start_rps_bo3(ctx, opponent: discord.Member = None):
    view = RPSBo3View(ctx, opponent)
    desc = f"{ctx.author.mention} started **Best of 3 Rock Paper Scissors!**\n"
    if opponent:
        desc += f"Opponent: {opponent.mention}\nFirst to 2 wins 🏆\nMake your choice 👇"
    else:
        desc += "You're playing against the Bot 🤖\nFirst to 2 wins 🏆\nMake your choice 👇"

    embed = discord.Embed(title="🪨📄✂️ Rock Paper Scissors - Best of 3", description=desc, color=discord.Color.blurple())
    await view.start_game()
