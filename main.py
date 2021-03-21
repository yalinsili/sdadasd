import discord
from discord.ext import commands
from discord.utils import get
import random
import string
import datetime
import config
import os
from pathlib import Path


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


def get_random_string(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


bot = commands.Bot(
    command_prefix=config.prefix,
    case_instensitive=True,
    owner_id=config.sahip_id,
    help_command=None,
    # self_bot=True #self bot için
)

# bot = commands.Bot(command_prefix="war") # prefixi configden aldığı için boş bu


@bot.event
async def on_ready():
    print(f"[+] Bot {bot.user.name} Actively Working on Account")
    await bot.change_presence(
        activity=discord.Game(
            name="Link Geçerim"
        )
    )


if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")


# bot.run(config.token, bot=False) #self bot için
bot.run(config.token)  # normal bot için
