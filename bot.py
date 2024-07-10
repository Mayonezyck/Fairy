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







'''def init_speech_services():
    voice_input_on = get_config("VOICE_INPUT_ON", False)
    tts_on = get_config("TTS_ON", False)
    speech2text, tts = None, None

    if voice_input_on:
        asr_model = get_config("STT_MODEL")

        asr_config = {}

        if asr_model == "AzureSTT":
            import api_keys
            asr_config = {
                "callback": print,
                "subscription_key": api_keys.AZURE_API_Key,
                "region": api_keys.AZURE_REGION,
            }
        else:
            asr_config = get_config(asr_model, {})

        speech2text = ASRFactory.get_asr_system(asr_model, **asr_config)

    if tts_on:
        tts_model = get_config("TTS_MODEL", "pyttsx3TTS")

        if tts_model == "AzureTTS":
            import api_keys
            tts_config = {
                "api_key": api_keys.AZURE_API_Key,
                "region": api_keys.AZURE_REGION,
                "voice": api_keys.AZURE_VOICE,
            }
        else:
            tts_config = get_config(tts_model, {})

        tts = TTSFactory.get_tts_engine(tts_model, **tts_config)

    return speech2text, tts'''

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
'''
@bot.command()
async def join_voice(ctx):
    await voice_channel.join(ctx)
@bot.command()
async def leave_voice(ctx):
    await voice_channel.leave(ctx)'''

#---------------------------------In development----------------------



#-----------------------------DEBUG ONLY----------------------------
async def DEBUG_printMessageInfo(message):
    line1 = f'MESSAGEAUTHOR:{message.author},BOTUSER{bot.user}'
    await message.channel.send(line1)

    ifMention = f'BOT MENTIONED?{bot.user.mentioned_in(message)} MESSAGE_MENTIONS:{message.mentions}'
    await message.channel.send(ifMention)

# Start the bot
llm_provider = get_config("LLM_PROVIDER")
llm_config = get_config(llm_provider, {})
system_prompt = get_config("SYSTEM_PROMPT")
llm_info = [llm_provider, llm_config, system_prompt]
#speech2text, tts = init_speech_services()
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = fairy.Fairy(testchannel = get_config("TESTCHANNEL"), llm_info = llm_info, intents=intents)
client.run(TOKEN)
