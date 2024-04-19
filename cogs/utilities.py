import discord
import aiohttp
from discord import app_commands, ui
from discord.ext import commands, tasks


class utilities(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ch_id = 0
        self.listening_status = False
        self.counter = 0

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


class RepeatMessage(ui.Modal, title="Repeat Message"):
    time_interval = ui.TextInput(
        label="Time Interval (Minutes) - float",
        style=discord.TextStyle.short,
        placeholder="0.1",
        required=True,
    )
    number_repetitions = ui.TextInput(
        label="Number of Repetitions - integer",
        style=discord.TextStyle.short,
        placeholder="3",
        required=True,
    )

    def __init__(self, message: discord.Message):
        super().__init__(timeout=None)
        self.message = message

    async def on_submit(self, interaction: discord.Interaction):
        if self.message.content == "":
            msg_author = self.message.author
            await self.interaction_check(interaction)
            await msg_author.send(content="Empty Message")

        else:

            @tasks.loop(
                minutes=float(self.time_interval.value),
                count=int(self.number_repetitions.value),
            )
            async def send_repeat_message():
                await self.message.channel.send(self.message.content)

            send_repeat_message.start()

            await interaction.response.send_message(
                content=f"Bot is repeating message every **{self.time_interval.value} minutes** for **{self.number_repetitions.value} times** !",
                ephemeral=True,
                view=StopRepeatButton(
                    send_repeat_message,
                    self.time_interval.value,
                    self.number_repetitions.value,
                ),
            )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        if isinstance(error, ValueError):
            await interaction.response.send_message(
                content="Wrong data type was received, please enter the correct data type",
                ephemeral=True,
            )
        if isinstance(error, AttributeError):
            interaction_author = interaction.user
            interaction_message = self.message.id
            interaction_guild = interaction.guild.id
            interaction_channel = interaction.channel.id
            await interaction_author.send(
                content=f"Cannot repeat message on https://discord.com/channels/{interaction_guild}/{interaction_channel}/{interaction_message} message"
            )


class StopRepeatButton(discord.ui.View):
    def __init__(self, loop, interval, count):
        super().__init__(timeout=None)
        self.loop = loop
        self.interval = interval
        self.count = count

    @discord.ui.button(
        label="Stop Repeating",
        emoji="🟥",
        style=discord.ButtonStyle.gray,
    )
    async def stop_repeat_message(
        self,
        interaction: discord.Interaction,
        Button: discord.ui.Button,
    ):
        self.loop.cancel()
        await interaction.response.edit_message(
            content=f"Bot stopped repeating message", view=None
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(utilities(bot))
