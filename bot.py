import yaml
import discord
from discord.ext import commands

def load_secret():
    with open("secret.yaml", "r") as f:
        secret = yaml.safe_load(f)
        return secret.get('DISCORD', default)


Discord_token = load_secret
# Define the bot and its command prefix
bot = commands.Bot(command_prefix='!')

# Event listener for when the bot has connected to the server
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Event listener for when a new member joins the server
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')

# Command for the bot to respond to
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

# Run the bot with your token

bot.run(load_secret())
