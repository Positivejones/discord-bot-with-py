import discord
from discord import app_commands 
from discord.ext import commands
import re
from dotenv import load_dotenv
import os
import random
import json
import requests
from insta import download_instagram_video
from rizz import me

with open('emojis.json','r') as f:
    emoji= json.load(f)


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
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Minecraft"))
#updates    
@bot.tree.command(name="what_new",description="update about my app")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def hello(interaction: discord.Interaction):
     await interaction.response.send_message(f"# Hello{interaction.user.mention} cutie. \n**•**we added **/afk** command for server to set that ur afk with a  reason "+"\n[Thank you for adding the app](https://d.ddinstagram.com/reel/C_iY37kI8u1/)")
#to download any video from instagram and tiktok
@bot.tree.command(name='d',description="to download a video from instagram and tiktok")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(url = "put the link here!")
async def download(interaction: discord.Interaction, url: str):
    if url.startswith("https://www.instagram.com/"):
        edited = re.sub(r'www\.', 'd.dd', url)
        medited = edited.split("?")[0]
        await interaction.response.send_message(f"{medited}")
    elif url.startswith("https://www.tiktok.com/") or url.startswith("https://vm.tiktok.com"):
        data = {"input_text": url}
        try:
            response = requests.post("https://api.quickvids.win/v1/shorturl/create", json=data)
            response.raise_for_status()
            if response.status_code == 200:
                vid = response.json()
                quickvid = vid['quickvids_url']
            else:
                quickvid = "Failed to shorten the link! Please try again later."
        except requests.RequestException as e:
            quickvid = f"Failed to shorten the link: {e}"

        await interaction.response.send_message(quickvid)
    else:
        await interaction.response.send_message("Invalid URL. Please enter a valid Instagram or TikTok URL.")

#my playlist command
@bot.tree.command(name="playlists", description="all my playlists if u want urs to be here contact afk_smta ")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(playlist="choice")
@app_commands.choices(playlist= [
    discord.app_commands.Choice(name='PARTY AT THE BEACH YAy', value=1),
    discord.app_commands.Choice(name='Homeless Without the m', value=2),
    discord.app_commands.Choice(name='Sheotz', value=3),
    #discord.app_commands.Choice(name='', value=1),
])
async def playl(interaction: discord.Interaction, playlist: discord.app_commands.Choice[int]):
    if playlist.value == 1:
        a = discord.Embed(title="Playlist <:spotify:1277464491109519391>")
        a.add_field(name="Jones3301's playlist <a:jojo:1277464516459892788>", value="[Click here](https://open.spotify.com/playlist/7jaKAb7LpoSKKWSqXfjld2?si=e105460e927a4745)")
        a.set_image(url="https://cdn.discordapp.com/attachments/760982527590006805/1277404807539331212/image.png")
    elif playlist.value == 2:
        a = discord.Embed(title="Playlist <:spotify:1277464491109519391>")
        a.add_field(name="Jones3301's playlist <a:jojo:1277464516459892788>", value="[Click here](https://open.spotify.com/playlist/19CuC2AcoOkejeBvuiE2tu?si=f179e010982746ff)")
        a.set_image(url="https://cdn.discordapp.com/attachments/760982527590006805/1277448920980787301/image.png")
    elif playlist.value == 3:
        a = discord.Embed(title="Playlist <:spotify:1277464491109519391>")
        a.add_field(name="Jones3301's playlist <a:jojo:1277464516459892788>", value="[Click here](https://open.spotify.com/playlist/0O0fMHGzgAcaFKLG2ufBzU?si=800fc699a154476c)")
        a.set_image(url="https://cdn.discordapp.com/attachments/760982527590006805/1277448956745482250/image.png")

    await interaction.response.send_message(embed=a)
    
#install teh video and send it to discord server 
@bot.tree.command(name="instagram",description="to save the video on server. and remember the name of the file always is salam.mp4")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def instagram(interaction:discord.Interaction,url:str):
    filename= "salam.mp4"
    owners=[725068306595446904,603299288159748108]
    if interaction.user.id not in owners:
        emb=discord.Embed(title='Error',color=discord.Color.red())
        emb.add_field(name="THIS COMMAND NOT FOR YOU!",value="you are not allowed to use this command <:idk:1281999974682464308>")
        emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/1280532050574839979/1282038677601521684/image_2024-09-07_190312755.png")
        await interaction.response.send_message(embed=emb)
        return
    await interaction.response.defer() # Defer the response
    download_instagram_video(url ,output_folder="videos")
# Construct the full path to the video file
    video_path = os.path.join("videos", filename)

# Check if the file exists
    if not os.path.exists(video_path):
        await interaction.followup.send(content=f"Video '{filename}' not found in the 'videos' folder.")
        return

# Send the video
    try:
        with open(video_path, "rb") as f:
            await interaction.followup.send(content="Video sent successfully!", file=discord.File(f, filename=filename))
    except Exception as e:
        await interaction.followup.send(content=f"Error sending video: {e}")

    try:
        os.remove(video_path)
        await interaction.followup.send(content="Video deleted from the folder!")
    except FileNotFoundError:
        await interaction.followup.send(content="Video was not found on the server!")
    except Exception as e:
        await interaction.followup.send(content=f"Error deleting video: {e}")
#show all servers the bot on         
@bot.tree.command(name="servers", description="See the servers the bot is on.")
async def servers(interaction: discord.Interaction):
    if interaction.user.id != 725068306595446904:
        emb=discord.Embed(title='Error',color=discord.Color.red())
        emb.add_field(name="THIS COMMAND NOT FOR YOU!",value="you are not allowed to use this command <:idk:1281999974682464308>")
        emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/1280532050574839979/1282038677601521684/image_2024-09-07_190312755.png")
        await interaction.response.send_message(embed=emb)
        return
    guild_list = "".join(f"\n**{guild.name}** (ID: {guild.id})" for guild in bot.guilds)
    await interaction.response.send_message(f"The bot is on these servers:\n{guild_list}")
#rizz video command
@bot.tree.command(name="rizz",description="choose a video")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(choose="choose a video")
@app_commands.choices(choose= [
    discord.app_commands.Choice(name='AAAAAAAAAAAAA', value=1),
    discord.app_commands.Choice(name='W rizz', value=2),
    discord.app_commands.Choice(name='Chinese girl', value=3),
    discord.app_commands.Choice(name='Roblox rizz', value=4),
    discord.app_commands.Choice(name='Kawaii', value=5),
    discord.app_commands.Choice(name='King nasir', value=6),
    #discord.app_commands.Choice(name='', value=1),
])
async def reaction(interaction: discord.Interaction,choose:discord.app_commands.Choice[int]):
	await me(choose,interaction)

afk_users = {}
@bot.tree.command(name="afk", description="Set your AFK status")
async def afk(interaction: discord.Interaction, reason: str = None):
    afk_users[interaction.user.id] = reason
    await interaction.response.send_message(f"You are now AFK. **{reason}**")

@bot.event
async def on_message(message):
    emo=emoji["hihihi"]
    if message.author == bot.user:
        return
    if message.author.id in afk_users:
        await message.channel.send(f"Welcome back, ``{message.author.name}``{emo}\n [Video](https://cdn.discordapp.com/attachments/1277317198041448539/1282205803067084841/salam.mp4)")
        del afk_users[message.author.id]

    for user_id, reason in afk_users.items():
        user = bot.get_user(user_id)
        if user.mentioned_in(message):
            await message.reply(f"Hey, ``{user.name}`` is AFK. Reason: **{reason}**")
            
            
@bot.tree.command(name="help",description="if any you need any help^^")
async def help(interaction:discord.Interaction):
    afk=discord.Embed(title=f"Hello {interaction.user.name}",color=discord.Color.blue(),description=f"{emoji["reply"]}if u need help **[Click here](https://discord.gg/XwmySkDSSy)**")
    afk.set_footer(text="Thanks")
    video=discord.File("./vid/input.mp4", filename="input.mp4")
    await interaction.response.defer()
    await interaction.followup.send(embed=afk,file=video )

bot.run(TOKEN)
