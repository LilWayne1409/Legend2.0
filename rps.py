import discord
from discord.ui import View, Button
import random

CHOICES = {
    "Rock": "🪨",
    "Paper": "📄",
    "Scissors": "✂️"
}

# =====================
# Single Round
# =====================
class SingleRPSButton(Button):
    def __init__(self, label, view):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.view = view

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        self.view.user_choice = self.label
        bot_choice = random.choice(list(CHOICES.keys()))

        wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
        if self.view.user_choice == bot_choice:
            result = "Tie!"
        elif wins[self.view.user_choice] == bot_choice:
            result = f"{user.mention} wins!"
        else:
            result = "Bot wins!"

        embed = discord.Embed(
            title="🕹️ Rock Paper Scissors",
            description=f"{user.mention} chose **{self.view.user_choice}**\n"
                        f"Bot chose **{bot_choice}**\n\n"
                        f"**{result}**",
            color=discord.Color.blurple()
        )
        await interaction.response.edit_message(embed=embed, view=None)
        self.view.stop()

class SingleRPSView(View):
    def __init__(self):
        super().__init__()
        self.user_choice = None
        for choice in CHOICES:
            self.add_item(SingleRPSButton(choice, self))

# =====================
# Best of 3
# =====================
class Bo3RPSView(View):
    def __init__(self, player, message):
        super().__init__(timeout=None)
        self.player = player
        self.message = message
        self.round = 1
        self.max_rounds = 3
        self.scores = {"player": 0, "bot": 0}
        self.current_choices = {}
        self.embed = discord.Embed(
            title=f"🕹️ Rock Paper Scissors - Round {self.round}",
            description="Choose one:",
            color=discord.Color.blurple()
        )
        for choice in CHOICES:
            self.add_item(Bo3RPSButton(choice, self))

    async def update_embed(self, interaction: discord.Interaction, round_result: str):
        desc = f"Round {self.round} result: {round_result}\n\n" \
               f"Score: {self.scores['player']} - {self.scores['bot']}\n\n" \
               f"Choose your move for the next round:" if self.round <= self.max_rounds else \
               f"Final Score: {self.scores['player']} - {self.scores['bot']}"
        self.embed.description = desc
        if self.round > self.max_rounds:
            # End result
            if self.scores['player'] > self.scores['bot']:
                final_text = f"🏆 {self.player.mention} wins the match!"
            elif self.scores['player'] < self.scores['bot']:
                final_text = "🏆 Bot wins the match!"
            else:
                final_text = "🎯 The match is a Tie!"
            self.embed.description = f"{final_text}\nFinal Score: {self.scores['player']} - {self.scores['bot']}"
            await interaction.response.edit_message(embed=self.embed, view=None)
            self.stop()
        else:
            self.round += 1
            await interaction.response.edit_message(embed=self.embed, view=self)

class Bo3RPSButton(Button):
    def __init__(self, label, view):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.view = view

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if user != self.view.player:
            await interaction.response.send_message("❌ You are not part of this game!", ephemeral=True)
            return

        user_choice = self.label
        bot_choice = random.choice(list(CHOICES.keys()))

        wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
        if user_choice == bot_choice:
            round_result = "Tie!"
        elif wins[user_choice] == bot_choice:
            round_result = f"{user.mention} wins this round!"
            self.view.scores['player'] += 1
        else:
            round_result = "Bot wins this round!"
            self.view.scores['bot'] += 1

        await self.view.update_embed(interaction, round_result)

# =====================
# Startfunktion
# =====================
async def start_rps_game(message: discord.Message, best_of_3=False):
    """
    Startet eine Runde Rock Paper Scissors gegen den Bot.
    best_of_3=True -> Best of 3 Modus
    """
    if not best_of_3:
        view = SingleRPSView()
        embed = discord.Embed(
            title="🕹️ Rock Paper Scissors",
            description="Choose one:",
            color=discord.Color.blurple()
        )
        await message.channel.send(embed=embed, view=view)
    else:
        view = Bo3RPSView(player=message.author, message=message)
        await message.channel.send(embed=view.embed, view=view)