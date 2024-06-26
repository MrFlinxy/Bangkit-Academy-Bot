import discord
import asyncio
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
            msg_author = (
                self.message.author
            )  # Warning: I am not sure why this code works
            await self.interaction_check(
                interaction
            )  # Warning: I am not sure why this code works
            await msg_author.send(
                content="Empty Message"
            )  # Warning: I am not sure why this code works

        else:

            @tasks.loop(
                minutes=float(self.time_interval.value),
                count=int(self.number_repetitions.value),
            )
            async def send_repeat_message():
                try:
                    await self.message.channel.send(self.message.content)
                except Exception as e:
                    if e.code == 50001:
                        if interaction.response.is_done() == False:
                            await interaction.response.send_message(
                                content=f"Bot has no Access to this channel",
                                ephemeral=True,
                            )

            send_repeat_message.start()

            if interaction.response.is_done() == False:
                await asyncio.sleep(2)
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
