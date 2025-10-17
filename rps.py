import random
import discord
from discord.ui import View, Button

CHOICES = {
    "Rock": "🪨",
    "Paper": "📄",
    "Scissors": "✂️"
}

# =====================
# Single Round RPS
# =====================
class RPSView(View):
    def __init__(self, ctx, timeout=30):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.user_choice = None
        for choice in CHOICES:
            self.add_item(RPSButton(choice, self))

    async def end_game(self, user_choice):
        self.user_choice = user_choice
        bot_choice = random.choice(list(CHOICES.keys()))
        wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}

        if user_choice == bot_choice:
            result = "Tie!"
        elif wins[user_choice] == bot_choice:
            result = f"{self.ctx.author.mention} wins!"
        else:
            result = "Bot wins!"

        embed = discord.Embed(
            title="🕹️ Rock Paper Scissors",
            description=f"{self.ctx.author.mention} chose {user_choice}\n"
                        f"Bot chose {bot_choice}\n\n"
                        f"**{result}**",
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
        if user != self.parent_view.ctx.author:
            await interaction.response.send_message("❌ You cannot play this game!", ephemeral=True)
            return
        await interaction.response.defer()
        await self.parent_view.end_game(self.label)


# =====================
# Best of 3 RPS
# =====================
class RPSBo3View(View):
    def __init__(self, ctx, timeout=30):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.player = ctx.author
        self.bot = ctx.bot.user
        self.scores = {self.player: 0, self.bot: 0}
        self.round = 1
        self.max_rounds = 3
        self.choices_this_round = {}
        self.setup_buttons()

    def setup_buttons(self):
        self.clear_items()
        for choice in CHOICES:
            self.add_item(RPSBo3Button(choice, self))

    async def round_result(self):
        p_choice = self.choices_this_round[self.player]
        b_choice = self.choices_this_round.get(self.bot, random.choice(list(CHOICES.keys())))
        wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}

        if p_choice == b_choice:
            result_text = "Tie!"
        elif wins[p_choice] == b_choice:
            result_text = f"{self.player.mention} wins this round!"
            self.scores[self.player] += 1
        else:
            result_text = f"Bot wins this round!"
            self.scores[self.bot] += 1

        embed = discord.Embed(
            title=f"Round {self.round} Result",
            description=f"{self.player.mention} chose {p_choice}\nBot chose {b_choice}\n\n**{result_text}**\n\n"
                        f"Score: {self.scores[self.player]} - {self.scores[self.bot]}",
            color=discord.Color.blurple()
        )
        await self.ctx.channel.send(embed=embed)

        self.round += 1
        self.choices_this_round = {}
        if self.round > self.max_rounds or max(self.scores.values()) > self.max_rounds // 2:
            # End result
            if self.scores[self.player] == self.scores[self.bot]:
                final_text = f"🎯 Tie! Both scored {self.scores[self.player]} points!"
            else:
                winner = self.player if self.scores[self.player] > self.scores[self.bot] else "Bot"
                final_text = f"🏆 {winner if winner=='Bot' else winner.mention} wins the match!\nScore: {self.scores[self.player]} - {self.scores[self.bot]}"
            final_embed = discord.Embed(title="RPS Best of 3 - Final Result", description=final_text, color=discord.Color.gold())
            await self.ctx.channel.send(embed=final_embed)
            self.stop()
        else:
            embed = discord.Embed(title=f"Round {self.round} - Rock Paper Scissors", description="Choose one:", color=discord.Color.blurple())
            await self.ctx.channel.send(embed=embed, view=self)
            self.setup_buttons()


class RPSBo3Button(Button):
    def __init__(self, label, parent_view):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if user != self.parent_view.player:
            await interaction.response.send_message("❌ You cannot play this game!", ephemeral=True)
            return
        if user in self.parent_view.choices_this_round:
            await interaction.response.send_message("⚠️ You already chose!", ephemeral=True)
            return

        self.parent_view.choices_this_round[user] = self.label
        await interaction.response.defer()

        # Bot wählt automatisch
        if self.parent_view.bot not in self.parent_view.choices_this_round:
            self.parent_view.choices_this_round[self.parent_view.bot] = random.choice(list(CHOICES.keys()))

        if all(player in self.parent_view.choices_this_round for player in [self.parent_view.player, self.parent_view.bot]):
            await self.parent_view.round_result()


# =====================
# Start function
# =====================
async def start_rps_game(message: discord.Message, best_of_3=False):
    if best_of_3:
        view = RPSBo3View(message)
    else:
        view = RPSView(message)
    embed = discord.Embed(title="🕹️ Rock Paper Scissors", description="Choose one:", color=discord.Color.blurple())
    await message.channel.send(embed=embed, view=view)