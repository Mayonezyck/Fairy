import yaml
import discord
import re
import os


from fairy.bot_configure import fairy
from fairy.bot_commands import voice_channel

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
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

In_Voice = True
live2d = None

# Creating bot instance with command prefix '!'
#bot = commands.Bot(command_prefix='!', intents=intents)
#-----------------------------Init---------------------------------


#-----------------------------Helper--------------------------------
async def getResponse(thisllm, user_input):
    print('Thinking...')
    return thisllm.chat(user_input)
async def getResponse_audio(thisllm, voice_channel, user_input):
    print('Thinking...in audio')
    vc = await voice_channel.connect()
    result = llm.chat_stream_audio(
        voice_channel,
        user_input,
        generate_audio_file=generate_audio_file,
        stream_audio_file=stream_audio_file,
    )
    await vc.disconnect()

async def mentioned_function(message):
    cleaned_message = re.sub(r'<@!?[0-9]+>', '', message.content).strip()
    response = f"Bot was mentioned! Message: {cleaned_message}"
    await message.channel.typing()
    if In_Voice:
        if message.author.voice:
            voice_channel = message.author.voice.channel
            await getResponse_audio(llm, voice_channel, cleaned_message)
        else:
            await message.channel.send('How can you listen if you are not in a voice channel?')
    else:
        llmresponse = await getResponse(llm, cleaned_message)
        await message.channel.send(llmresponse)



#------------------------------Tested Events-----------------------
# Event that triggers when the bot is ready
#-----------------------------Tested Commands----------------------
#---------------------------------In development----------------------



#-----------------------------DEBUG ONLY----------------------------


# Start the bot
llm_provider = get_config("LLM_PROVIDER")
llm_config = get_config(llm_provider, {})
system_prompt = get_config("SYSTEM_PROMPT")
llm_info = [llm_provider, llm_config, system_prompt]
tts_info = [get_config("SPEECH_KEY"),get_config("SERVICE_REGION"),get_config("VOICE_NAME")]
#speech2text, tts = init_speech_services()
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = fairy.Fairy(testchannel = get_config("TESTCHANNEL"), llm_info = llm_info, tts_info = tts_info, intents=intents)
client.run(TOKEN)
