import discord
from discord.ui import View, Button
import random

CHOICES = {
    "Rock": "🪨",
    "Paper": "📄",
    "Scissors": "✂️"
}

# =====================
# Normal RPS View (einzelne Runde)
# =====================
class RPSView(View):
    def __init__(self, ctx, opponent=None, timeout_duration=30):
        super().__init__(timeout=timeout_duration)
        self.ctx = ctx
        self.opponent = opponent
        self.choices = {}
        self.result_sent = False

        # Buttons für Rock, Paper, Scissors
        self.add_item(RPSButton("Rock", "🪨", discord.ButtonStyle.primary, self))
        self.add_item(RPSButton("Paper", "📄", discord.ButtonStyle.success, self))
        self.add_item(RPSButton("Scissors", "✂", discord.ButtonStyle.danger, self))

    async def on_timeout(self):
        if self.result_sent:
            return
        # Spieler, die nicht gewählt haben, bekommen zufällige Auswahl
        players = [self.ctx.author]
        if self.opponent:
            players.append(self.opponent)
        for user in players:
            if user not in self.choices:
                self.choices[user] = random.choice(list(CHOICES.keys()))
        await self.show_result()

    async def show_result(self):
        self.result_sent = True
        author_choice = self.choices[self.ctx.author]
        opponent = self.opponent or self.ctx.bot.user
        opponent_choice = self.choices.get(opponent, random.choice(list(CHOICES.keys())))

        # Gewinner bestimmen
        result = self.determine_winner(author_choice, opponent_choice, opponent)

        embed = discord.Embed(
            title="🕹️ Rock Paper Scissors Result",
            description=f"{self.ctx.author.mention} chose {author_choice}\n"
                        f"{opponent.mention if self.opponent else 'Bot'} chose {opponent_choice}\n\n"
                        f"**{result}**",
            color=discord.Color.blurple()
        )
        await self.ctx.send(embed=embed)
        self.stop()

    def determine_winner(self, choice1, choice2, opponent):
        if choice1 == choice2:
            return "Tie!"
        wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
        if wins[choice1] == choice2:
            return f"{self.ctx.author.mention} wins!"
        else:
            return f"{opponent.mention if self.opponent else 'Bot'} wins!"

class RPSButton(Button):
    def __init__(self, label, emoji, style, view):
        super().__init__(label=label, emoji=emoji, style=style)
        self.parent_view = view

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        view = self.parent_view

        # Prüfen, ob Spieler dabei ist
        if user != view.ctx.author and user != view.opponent:
            await interaction.response.send_message("❌ You are not part of this game!", ephemeral=True)
            return

        view.choices[user] = self.label
        await interaction.response.send_message(f"✅ {user.mention} chose {self.label}", ephemeral=True)

        # Wenn alle Spieler gewählt haben, Ergebnis anzeigen
        players = [view.ctx.author]
        if view.opponent:
            players.append(view.opponent)
        if all(player in view.choices for player in players):
            await view.show_result()

# =====================
# Best of 3 View
# =====================
class RPSBo3View(View):
    def __init__(self, ctx, opponent=None, timeout=30):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.player1 = ctx.author
        self.player2 = opponent if opponent else ctx.bot.user
        self.scores = {self.player1: 0, self.player2: 0}
        self.round = 1
        self.max_rounds = 3
        self.choices_this_round = {}
        self.setup_buttons()

    def setup_buttons(self):
        self.clear_items()
        for choice, emoji in CHOICES.items():
            style = discord.ButtonStyle.primary if choice == "Rock" else discord.ButtonStyle.success if choice == "Paper" else discord.ButtonStyle.danger
            self.add_item(RPSBo3Button(choice, emoji, style, self))

    async def round_result(self):
        p1_choice = self.choices_this_round[self.player1]
        p2_choice = self.choices_this_round.get(self.player2, random.choice(list(CHOICES.keys())))

        # Gewinner bestimmen
        if p1_choice == p2_choice:
            result_text = "Tie!"
        else:
            wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
            if wins[p1_choice] == p2_choice:
                result_text = f"{self.player1.mention} wins this round!"
                self.scores[self.player1] += 1
            else:
                result_text = f"{self.player2.mention if isinstance(self.player2, discord.Member) else 'Bot'} wins this round!"
                self.scores[self.player2] += 1

        embed = discord.Embed(
            title=f"Round {self.round} Result",
            description=f"{self.player1.mention} chose {p1_choice}\n"
                        f"{self.player2.mention if isinstance(self.player2, discord.Member) else 'Bot'} chose {p2_choice}\n\n"
                        f"**{result_text}**\n\n"
                        f"Score: {self.scores[self.player1]} - {self.scores[self.player2]}",
            color=discord.Color.blurple()
        )
        await self.ctx.send(embed=embed)

        # Nächste Runde oder Match Ende
        self.round += 1
        if self.round > self.max_rounds or max(self.scores.values()) > self.max_rounds // 2:
            winner = max(self.scores, key=self.scores.get)
            if self.scores[self.player1] == self.scores[self.player2]:
                final_text = f"🎯 Tie! Both scored {self.scores[self.player1]} points!"
            else:
                final_text = f"🏆 {winner.mention if isinstance(winner, discord.Member) else 'Bot'} wins the match!\nScore: {self.scores[self.player1]} - {self.scores[self.player2]}"
            final_embed = discord.Embed(title="RPS Best of 3 - Final Result", description=final_text, color=discord.Color.gold())
            await self.ctx.send(embed=final_embed)
            self.stop()
        else:
            self.choices_this_round = {}
            self.setup_buttons()
            embed = discord.Embed(title=f"Round {self.round} - Rock Paper Scissors", description="Choose one:", color=discord.Color.blurple())
            await self.ctx.send(embed=embed, view=self)

class RPSBo3Button(Button):
    def __init__(self, label, emoji, style, view):
        super().__init__(label=label, emoji=emoji, style=style)
        self.parent_view = view

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        view = self.parent_view

        # Prüfen, ob Spieler dabei ist
        if user != view.player1 and user != view.player2:
            await interaction.response.send_message("❌ You are not part of this game!", ephemeral=True)
            return

        if user in view.choices_this_round:
            await interaction.response.send_message("⚠️ You already chose!", ephemeral=True)
            return

        view.choices_this_round[user] = self.label
        await interaction.response.send_message(f"✅ {user.mention} chose {self.label}", ephemeral=True)

        # Bot wählt automatisch, falls er der Gegner ist
        if view.player2 == view.ctx.bot.user and view.player2 not in view.choices_this_round:
            view.choices_this_round[view.player2] = random.choice(list(CHOICES.keys()))

        # Wenn beide gewählt haben, Ergebnis berechnen + nächste Runde starten
        players = [view.player1, view.player2]
        if all(player in view.choices_this_round for player in players):
            await view.round_result()