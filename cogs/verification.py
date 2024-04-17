import discord
from discord import app_commands
from discord.ext import commands


class verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ch_id = 0
        self.listening_status = False
        self.counter = 0

    @app_commands.command(name="verification", description="Verification")
    async def verification(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Verification")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(verification(bot))
