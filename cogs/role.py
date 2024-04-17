import discord
from discord import app_commands
from discord.ext import commands


class role(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ch_id = 0
        self.listening_status = False
        self.counter = 0

    @app_commands.command(name="role", description="Role")
    async def role(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Role")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(role(bot))
