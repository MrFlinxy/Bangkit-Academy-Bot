<div align="center">
<p>
  <a href="https://grow.google/intl/id_id/bangkit/">
    <img alt="Bangkit" src="./Assets/bangkit.png" width="360">
  </a>
</p>
<h1>Bangkit Academy Bot</h1>

</div>

## Pre-requisites

- <a href="https://python.org/">Python3</a> (Developed in Python 3.12.3)
- Discord Bot Token (<a href="https://youtu.be/UYJDKSah-Ww?si=klfbiOqFP16M5ms9&t=135">See this tutorial video for setting up Discord Bot</a>)
  \*Note: make sure the bot is inside the Discord Server

## How to use

1. Clone the repository

```console
git clone https://github.com/MrFlinxy/Bangkit-Academy-Bot.git
```

2. Create python virtual environment

```console
python3 -m venv bangkitbot
```

3.1. Activate the python virtual environment (**Windows**)

```console
python -m venv bangkitbot
cd bangkitbot\Scripts
activate
```

3.2. Activate the python virtual environment (**Linux**)

```console
python3 -m venv bangkitbot
. bangkitbot/bin/activate
```

4. Install the required python packages from requirements.txt

```console
pip install -r requirements.txt
```

5. Create .env file

```console
echo TOKEN="<YOUR_BOT_TOKEN>" > .env
```

6.1. Run the Bangkit Bot (**Windows**)

```console
python bangkitbot.py
```

6.2. Run the Bangkit Bot (**Linux**)

```console
python3 bangkitbot.py
```

7. Please reload the bot by running the following command inside the Discord server

```console
/reloadbangkitbot
```

To see available commands, run the following command inside the Discord server

```console
/bangkitbot
```

## Bot Commands

- List the bot commands

```console
/bangkitbot
```

- Listen a stage channel to count the attendances

```console
/radioselect
```

- Reloading / resyncing the bot commands

```console
/reloadbangkitbot
```

## Issues

- "**Start New Listening**" or "**Continue Listening to the Previous Listening**" after the bot stopped listening has not been implemented yet.
- There is still no method to reset the data that has been collected, so the Bot will continue the previous listening to same graph in the same day (even if the stage channel is different).
- If an error is encountered, try to reload the bot with `/reloadbangkitbot` command.
- If you did not see any commands available, try to kick the bot from Discord server, and then re-adding the bot to Discord server.

## Todo

###### <em>Only if i have the time, power, and willingness to do these</em>

- Improving Radio Listening
- Role Management
- Channel Management
- Discord Bot Dashboard
- Bangkit Discord Verification
- Utilities (Get user data, get user avatar, repeating a message periodically, etc)
