import discord
from discord import app_commands
from discord.ext import commands


class utilities(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ch_id = 0
        self.listening_status = False
        self.counter = 0

    @app_commands.command(name="utilities", description="Utilities")
    async def utilities(self, interaction: discord.Interaction):
        print(type(0x1ABC9C))
        await interaction.response.send_message(content="Utilities")

    @app_commands.command(name="send_embed", description="Send an Embed message")
    async def send_embed(
        self,
        interaction: discord.Interaction,
        title: str,
        url: str = None,
        description: str = None,
        color: int = 0x5865F2,
    ):
        await interaction.response.send_message(
            embed=discord.Embed(
                title=title,
                url=url,
                description=description,
                color=color,
            )
        )

    # Anti Discord Polling Creation
    @commands.Cog.listener()
    async def on_message(self, message):
        role_id_list = [1060927000723865610, 1220559793358504096]
        try:
            roles_get = [
                discord.utils.get(message.guild.roles, id=i) for i in role_id_list
            ]
            author_roles = message.author.roles
            intersect_set = set(roles_get).intersection(set(author_roles))

            if message.attachments == []:
                if (
                    message.type == discord.MessageType.chat_input_command
                    or message.type == discord.MessageType.reply
                ):
                    return
                if message.content == "":
                    if len(intersect_set) == 0:
                        await message.delete()
        except:
            pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(utilities(bot))
