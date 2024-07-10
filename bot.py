import yaml
import discord
from discord.ext import commands
import re

def load_secret():
    with open("secret.yaml", "r") as f:
        secret = yaml.safe_load(f)
        return secret.get('DISCORD')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = load_secret()

# Intents are required to read messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Creating bot instance with command prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the function to be called when the bot is mentioned
def mentioned_function(message_content):
    print(f"Bot was mentioned! Message: {message_content}")

# Event that triggers when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

# Event that triggers on new message
@bot.event
async def on_message(message):
    # Check if the message mentions the bot
    if bot.user.mentioned_in(message):
        # Remove the mention part from the message content
        cleaned_message = re.sub(r'<@!?[0-9]+>', '', message.content).strip()
        mentioned_function(cleaned_message)
    # Process commands if any
    await bot.process_commands(message)

# Start the bot
bot.run(TOKEN)
