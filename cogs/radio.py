import discord
import pickle
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from matplotlib import pyplot as plt
from os.path import exists
from pathlib import Path
import pandas as pd

file_fmt = datetime.now().strftime("%d_%b_%Y")
timestamp_format = "%d.%b %Y %H:%M:%S.%f"
csv_filename = f"collected_data/{file_fmt}/{file_fmt}"
pickle_filename = f"collected_data/{file_fmt}/{file_fmt}"
Path(f"collected_data/{file_fmt}").mkdir(parents=True, exist_ok=True)


def change_states(value):
    radio.states = value


def change_ch_id(value):
    radio.ch_id = value


def change_cmd_called(value):
    radio.cmd_called = value


def get_unique_member(bot, memberjoin_set):
    member_list = []
    x = bot.get_channel(radio.ch_id)

    for i in x.members:
        member_list.append(i.name)

    memberjoin_set.update(member_list)


class SelectMenu(discord.ui.Select):

    def __init__(self, stagelist, bot):
        self.stagelist = stagelist
        self.bot = bot
        stages = [
            discord.SelectOption(label=i.name, value=i.id, emoji="🔊")
            for i in self.stagelist
        ]
        super().__init__(
            placeholder="Select a Stage Channel to listen",
            max_values=1,
            min_values=1,
            options=stages,
        )

    async def callback(self, interaction: discord.Interaction):
        change_ch_id(int(self.values[0]))
        change_cmd_called(False)
        change_states(True)

        if exists(pickle_filename + ".pkl"):
            saved_pickle = open(
                pickle_filename + ".pkl",
                "rb",
            )
            memberjoin = pickle.load(saved_pickle)
            get_unique_member(self.bot, memberjoin)
            saved_pickle.close()

        else:
            memberjoin = set()
            get_unique_member(self.bot, memberjoin)
            write_pickle = open(
                pickle_filename + ".pkl",
                "wb",
            )
            pickle.dump(memberjoin, write_pickle)
            write_pickle.close()

        embed = discord.Embed(
            title=f"Bot is Listening to <#{int(self.values[0])}>",
            url=None,
            description=None,
            color=0x1ABC9C,
        )

        await interaction.response.edit_message(embed=embed, view=ListeningButton())


class Select(discord.ui.View):
    def __init__(self, stagelist, bot):
        super().__init__()
        self.stagelist = stagelist
        self.bot = bot
        self.add_item(SelectMenu(stagelist, bot))


class ListeningButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Get Graph", emoji="📈", style=discord.ButtonStyle.blurple, custom_id="0"
    )
    async def get_graph(
        self, interaction: discord.Interaction, Button: discord.ui.Button
    ):
        if exists(csv_filename + ".csv"):
            colnames = ["datetime", "listeners", "uniqueUser"]
            radio_df = pd.read_csv(
                csv_filename + ".csv",
                names=colnames,
                index_col="datetime",
                header=None,
                parse_dates=True,
            )

            radio_df[["listeners", "uniqueUser"]].plot(figsize=(19.2, 10.8))
            plt.title(f"Radio Bangkit {file_fmt} Listeners")
            plt.grid(color="gray", linestyle="-", linewidth=0.2)
            plt.figtext(0.1, 0.92, f"Listeners peak = {max(radio_df['listeners'])}")
            plt.figtext(0.1, 0.9, f"Unique User count = {max(radio_df['uniqueUser'])}")
            plt.savefig(f"collected_data/{file_fmt}/{file_fmt}_graph.png")

            with open(f"collected_data/{file_fmt}/{file_fmt}_graph.png", "rb") as file:
                await interaction.response.send_message(
                    None,
                    file=discord.File(file, f"{file_fmt}_graph.png"),
                    ephemeral=True,
                )

        else:
            embed = discord.Embed(
                title=f"No Data Available",
                url=None,
                description="Please start bot to listen first.",
                color=0xE67E22,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="Stop Listening",
        emoji="❌",
        style=discord.ButtonStyle.gray,
        custom_id="1",
    )
    async def stop_listen(
        self, interaction: discord.Interaction, Button: discord.ui.Button
    ):
        if radio.ch_id != 0:

            if exists(csv_filename + ".csv"):
                colnames = ["datetime", "listeners", "uniqueUser"]
                radio_df = pd.read_csv(
                    csv_filename + ".csv",
                    names=colnames,
                    index_col="datetime",
                    header=None,
                    parse_dates=True,
                )

                embed = discord.Embed(
                    title=f"Bot Stopped Listening to <#{radio.ch_id}>",
                    url=None,
                    description=f"Listeners peak : **{max(radio_df['listeners'])}**\nUnique User count : **{max(radio_df['uniqueUser'])}**",
                    color=0xFF0000,
                )

                radio_df[["listeners", "uniqueUser"]].plot(figsize=(19.2, 10.8))
                plt.title(f"Radio Bangkit {file_fmt} Listeners")
                plt.grid(color="gray", linestyle="-", linewidth=0.2)
                plt.figtext(0.1, 0.92, f"Listeners peak = {max(radio_df['listeners'])}")
                plt.figtext(
                    0.1, 0.9, f"Unique User count = {max(radio_df['uniqueUser'])}"
                )
                plt.savefig(f"collected_data/{file_fmt}/{file_fmt}_graph.png")

                with open(
                    f"collected_data/{file_fmt}/{file_fmt}_graph.png", "rb"
                ) as file:
                    await interaction.response.send_message(
                        embed=embed,
                        file=discord.File(file, f"{file_fmt}_graph.png"),
                        ephemeral=False,
                    )

                change_states(False)
                change_ch_id(0)

            else:
                embed = discord.Embed(
                    title=f"Bot does not have any data",
                    url=None,
                    description=f"Please wait until the bot have some data",
                    color=0xE67E22,
                )
                await interaction.response.send_message(
                    embed=embed, ephemeral=True, view=ForceStopButton()
                )

        else:
            embed = discord.Embed(
                title=f"Bot Already Stopped Listening!",
                url=None,
                description=None,
                color=0x000000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class ForceStopButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="FORCE STOP",
        emoji="⚠️",
        style=discord.ButtonStyle.red,
        custom_id="2",
    )
    async def stop_listen(
        self, interaction: discord.Interaction, Button: discord.ui.Button
    ):
        if radio.ch_id != 0:
            embed = discord.Embed(
                title=f"FORCE STOPPED BOT!",
                url=None,
                description="Some data might have been corrupted",
                color=0xFF0000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)

            change_states(False)
            change_ch_id(0)


class radio(commands.Cog):
    ch_id = 0
    states = False
    cmd_called = False

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.counter = 0
        self.stagelist = []

        for guild in bot.guilds:
            for channel in guild.stage_channels:
                self.stagelist.append(channel)

    @app_commands.command(name="radioselect", description="radioselect")
    async def radioselect(self, interaction: discord.Interaction):
        if self.states == False:
            if self.cmd_called == False:
                if len(self.stagelist) != 0:
                    change_cmd_called(True)
                    await interaction.response.send_message(
                        view=Select(self.stagelist, self.bot)
                    )
                else:
                    await interaction.response.send_message(
                        content="Bot cannot find any accessible Stage Channel. Try Reloading the bot by ```/reloadbangkitbot```",
                        ephemeral=True,
                    )
            else:
                await interaction.response.send_message(
                    content="Same command is already called, please finish the unfinished command",
                    ephemeral=True,
                )

        else:
            embed = discord.Embed(
                title=f"Bot is already listening to <#{self.ch_id}>",
                url=None,
                description=None,
                color=0xFF0000,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if radio.states == True:
            if before is None or after is None:
                pass

            if after.channel is not None:
                if after.channel.id == radio.ch_id:
                    saved_pickle = open(pickle_filename + ".pkl", "rb")
                    memberjoin = pickle.load(saved_pickle)

                    memberjoin.add(member.name)

                    timestamp = pd.to_datetime(
                        datetime.now().strftime(timestamp_format)
                    )

                    new_row = pd.DataFrame(
                        [[timestamp, len(after.channel.listeners), len(memberjoin)]],
                    )

                    df = pd.DataFrame()
                    df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
                    df.to_csv(
                        csv_filename + ".csv",
                        mode="a",
                        index=False,
                        header=False,
                    )

                    write_pickle = open(pickle_filename + ".pkl", "wb")
                    pickle.dump(memberjoin, write_pickle)
                    write_pickle.close()

            if before.channel is not None:
                if before.channel.id == radio.ch_id:
                    saved_pickle = open(pickle_filename + ".pkl", "rb")
                    memberjoin = pickle.load(saved_pickle)

                    timestamp = pd.to_datetime(
                        datetime.now().strftime(timestamp_format)
                    )

                    new_row = pd.DataFrame(
                        [[timestamp, len(before.channel.listeners), len(memberjoin)]],
                    )

                    df = pd.DataFrame()
                    df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
                    df.to_csv(
                        csv_filename + ".csv",
                        mode="a",
                        index=False,
                        header=False,
                    )

                    write_pickle = open(pickle_filename + ".pkl", "wb")
                    pickle.dump(memberjoin, write_pickle)
                    write_pickle.close()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(radio(bot))
