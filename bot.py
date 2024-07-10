import yaml
import discord
import re
from discord.ext import commands

#Load Token from secret file
def load_secret():
    with open("secret.yaml", "r") as f:
        secret = yaml.safe_load(f)
        return secret.get('DISCORD')


TOKEN = load_secret()
TESTCHANNEL = 1260450089239838804
# Intents are required to read messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True



# Creating bot instance with command prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents)

#-----------------------------Helper--------------------------------
# Define the function to be called when the bot is mentioned
async def mentioned_function(message):
    cleaned_message = re.sub(r'<@!?[0-9]+>', '', message.content).strip()
    response = f"Bot was mentioned! Message: {cleaned_message}"
    await message.channel.send(response)

def shouldIgnore(message):
    if message.author == bot.user or message.channel.id != TESTCHANNEL:
        return True
    return False

#------------------------------Tested Events-----------------------
# Event that triggers when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

# Event that triggers on new message
@bot.event
async def on_message(message):
    if shouldIgnore(message):return
    await DEBUG_printMessageInfo(message)
    if bot.user.mentioned_in(message):
        await mentioned_function(message)
    await bot.process_commands(message)

#-----------------------------Tested Commands----------------------
#join voice channel
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel}')
    else:
        await ctx.send("You are not connected to a voice channel.")
#leave voice channel
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I am not in a voice channel.")

#---------------------------------In development----------------------

@bot.command
async def help(message):
    await message.channel.send('?Someone did not write the help file yet')

#----------ChatBot Connet-------
class LLM_PIPE:
    def __init__():
        
    def chat(prompt):

        full_response = self._send_message_to_agent(
            prompt, callback_function=print
        )

        return full_response

#-----------------------------DEBUG ONLY----------------------------
async def DEBUG_printMessageInfo(message):
    line1 = f'MESSAGEAUTHOR:{message.author},BOTUSER{bot.user}'
    await message.channel.send(line1)

    ifMention = f'BOT MENTIONED?{bot.user.mentioned_in(message)} MESSAGE_MENTIONS:{message.mentions}'
    await message.channel.send(ifMention)

# Start the bot
bot.run(TOKEN)
