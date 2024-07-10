import yaml
import discord
import re
import os
from discord.ext import commands
from llm.llm_factory import LLMFactory

#Load Token from secret file
def load_secret():
    with open("secret.yaml", "r") as f:
        secret = yaml.safe_load(f)
        return secret.get('DISCORD')
def load_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, "conf.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
def get_config(key, default=None):
    return config.get(key, default)

config = load_config()
TOKEN = load_secret()

# Intents are required to read messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True



# Creating bot instance with command prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents)
#-----------------------------Init---------------------------------
def init_llm():

    llm_provider = get_config("LLM_PROVIDER")
    llm_config = get_config(llm_provider, {})
    system_prompt = get_config("SYSTEM_PROMPT")
    llm = LLMFactory.create_llm(llm_provider=llm_provider, SYSTEM_PROMPT=system_prompt, **llm_config)
    return llm


#-----------------------------Helper--------------------------------
async def getResponse(thisllm, user_input):
    print('Thinking...')
    return thisllm.chat(user_input)

async def mentioned_function(message):
    cleaned_message = re.sub(r'<@!?[0-9]+>', '', message.content).strip()
    response = f"Bot was mentioned! Message: {cleaned_message}"
    await message.channel.typing()
    llmresponse = await getResponse(llm, cleaned_message)
    await message.channel.send(llmresponse)

def shouldIgnore(message):
    if message.author == bot.user or message.channel.id != get_config("TESTCHANNEL"):
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
    #await DEBUG_printMessageInfo(message)
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



#-----------------------------DEBUG ONLY----------------------------
async def DEBUG_printMessageInfo(message):
    line1 = f'MESSAGEAUTHOR:{message.author},BOTUSER{bot.user}'
    await message.channel.send(line1)

    ifMention = f'BOT MENTIONED?{bot.user.mentioned_in(message)} MESSAGE_MENTIONS:{message.mentions}'
    await message.channel.send(ifMention)

# Start the bot
llm = init_llm()
bot.run(TOKEN)
