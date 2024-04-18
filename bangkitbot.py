import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import Literal
from os import getenv
from cogs.radio import ListeningButton
from cogs.text_ready import bangkit_bot_ready


load_dotenv()
bot_token = getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class BangkitBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cogslist = [
            "cogs.channel",
            "cogs.radio",
            "cogs.role",
            "cogs.utilities",
            "cogs.verification",
        ]

    async def on_ready(self):
        print("### ====================")
        print("### Syncing commands...")
        x = await self.tree.sync()
        print(f"### Synced {str(len(x))} commands")
        bangkit_bot_ready()
        print("### ====================")

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)
        self.add_view(ListeningButton())


bot = BangkitBot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
bot.remove_command("help")


@bot.tree.command(name="reloadbangkitbot", description="Reloading Cogs File")
async def reloadbangkitbot(
    interaction: discord.Interaction,
    cog: Literal[
        "cogs.channel",
        "cogs.radio",
        "cogs.role",
        "cogs.utilities",
        "cogs.verification",
    ] = None,
):
    if cog == None:
        for i in [
            "cogs.channel",
            "cogs.radio",
            "cogs.role",
            "cogs.utilities",
            "cogs.verification",
        ]:
            await bot.reload_extension(name=i)
        await interaction.response.send_message(
            content=f"Successfully reloading **All cog files**", ephemeral=True
        )
    else:
        await bot.reload_extension(name=cog)
        await interaction.response.send_message(
            content=f"Successfully reloading **{cog}.py**", ephemeral=True
        )


@bot.tree.command(name="bangkitbot", description="List all commands")
async def bangkitbot(interaction: discord.Interaction):
    embed = discord.Embed(
        title="BangkitBot Commands",
        url=None,
        description=None,
        color=0xFF0000,
    )
    thumbnail_file = discord.File("Assets/bangkit_logo.png", filename="bangkitlogo.png")
    embed.set_thumbnail(
        url="attachment://bangkitlogo.png",
    )
    embed.add_field(
        name="- Show bot commands",
        value="```/bangkitbot```Showing this bot message",
        inline=False,
    )
    embed.add_field(
        name="⠀",
        value="",
        inline=False,
    )
    embed.add_field(
        name="- Listen to Stage Channel",
        value="```/radioselect```",
        inline=False,
    )
    embed.add_field(
        name="⠀",
        value="",
        inline=False,
    )
    embed.add_field(
        name="- Reload Bot Commands",
        value="```/reloadbangkitbot```",
        inline=False,
    )
    embed.set_footer(text="\n⠀\n⠀\nBy Discord Manager - Bangkit Academy 2024 Batch 1")
    await interaction.response.send_message(
        file=thumbnail_file, embed=embed, ephemeral=True
    )


### Context Menu ###
# Repeat Message
@bot.tree.context_menu(name="Repeat Message")
async def repeat_message(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(
        f"This is your message: \n{message.author}: {message.content}", ephemeral=False
    )


# Get User Avatar
@bot.tree.context_menu(name="Get User Avatar")
async def get_avatar(interaction: discord.Interaction, user: discord.Member):
    bot.add_view(ListeningButton())
    await interaction.response.send_message(content=user.avatar, ephemeral=False)


bot.run(bot_token)
