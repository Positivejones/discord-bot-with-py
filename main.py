import discord
from discord import app_commands 
from discord.ext import commands
import re
from dotenv import load_dotenv
import os
import random
import requests
import json


load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="*",intents= discord.Intents.all())

@bot.event
async def on_ready():
    print('im here')
    try: 
         synced = await bot.tree.sync()
         print(f"synced {len(synced)} command(s)")
    except Exception as e:
         print(e)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Mini game"))

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
     await interaction.response.send_message("hello")

@bot.tree.command(name='download')
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(url = "put the link here!")
async def instagram(interaction: discord.Integration, url:str):
    edited = re.sub(r'www\.', 'd.dd', url)
    medited = edited.split("?")[0]
    await interaction.response.send_message(f"{medited}")


@bot.tree.command(name="reaction")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def reaction(interaction: discord.Interaction):
     liste= ["https://quickvids.app/rOKGM_BU","https://d.ddinstagram.com/reel/C-mAXeRtZBd/","https://d.ddinstagram.com/reel/C-bPIpXv45y/"]
     a = random.choice(liste)
     await interaction.response.send_message(f"{a}")

@bot.tree.command(name='tiktok')
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(url="put the link here!")
async def tik(interaction: discord.Interaction, url:str):
    data = {"input_text": url}
    response = requests.post("https://api.quickvids.win/v1/shorturl/create", json=data)
    response.raise_for_status()

    if response.status_code == 200:
        vid = response.json()
        quickvid = vid['quickvids_url'] 
    else:
        quickvid = "Failed to shorten the link! Please try again later."

    await interaction.response.send_message(quickvid)


@bot.tree.command(name="hi")
@app_commands.describe(playlist="choice ")
@app_commands.choices(playlist= [
    discord.app_commands.Choice(name='PARTY AT THE BEACH YAy', value=1),
    discord.app_commands.Choice(name='Homeless Without the m', value=2),
    discord.app_commands.Choice(name='Sheotz', value=3),
    #discord.app_commands.Choice(name='', value=1),
])
async def playl(interaction: discord.Integration, playlist: discord.app_commands.Choice[int]):
    if playlist.value == 1:
        a = discord.Embed(title="Playlist <a:5769_JotaroDance:987774877433991168>")
        a.add_field(name="Jones3301's playlist <a:pepemexican:980596561937596426>", value="[Click here](https://open.spotify.com/playlist/7jaKAb7LpoSKKWSqXfjld2?si=e105460e927a4745)")
        a.set_image(url="https://cdn.discordapp.com/attachments/760982527590006805/1277404807539331212/image.png")
    elif playlist.value == 2:
        a = discord.Embed(title="Playlist <a:5769_JotaroDance:987774877433991168>")
        a.add_field(name="Jones3301's playlist <a:pepemexican:980596561937596426>", value="[Click here](https://open.spotify.com/playlist/19CuC2AcoOkejeBvuiE2tu?si=f179e010982746ff)")
        a.set_image(url="https://cdn.discordapp.com/attachments/760982527590006805/1277448920980787301/image.png")
    elif playlist.value == 3:
        a = discord.Embed(title="Playlist <a:5769_JotaroDance:987774877433991168>")
        a.add_field(name="Jones3301's playlist <a:pepemexican:980596561937596426>", value="[Click here](https://open.spotify.com/playlist/0O0fMHGzgAcaFKLG2ufBzU?si=800fc699a154476c)")
        a.set_image(url="https://cdn.discordapp.com/attachments/760982527590006805/1277448956745482250/image.png")

    await interaction.response.send_message(embed=a)
    



    await bot.tree.sync()
bot.run(TOKEN)