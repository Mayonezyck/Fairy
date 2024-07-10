import yaml
import discord
import re
import os
from discord.ext import commands
from llm.llm_factory import LLMFactory
from tts.tts_factory import TTSFactory
from asr.asr_factory import ASRFactory
from tts import stream_audio
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
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
In_Voice = True
live2d = None

# Creating bot instance with command prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents)
#-----------------------------Init---------------------------------
def init_llm():

    llm_provider = get_config("LLM_PROVIDER")
    llm_config = get_config(llm_provider, {})
    system_prompt = get_config("SYSTEM_PROMPT")
    llm = LLMFactory.create_llm(llm_provider=llm_provider, SYSTEM_PROMPT=system_prompt, **llm_config)
    return llm

def init_speech_services():
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

    return speech2text, tts
#-----------------------------Voice--------------------------------
async def speak_local(voice_channel, text, on_speak_start_callback=None, on_speak_end_callback=None):
    filepath = self.generate_audio(text)
    voice_channel = await voice_channel.connect()
    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filepath))
    #self.__remove_file(filepath)
    while voice_channel.is_playing():
        sleep(.1)
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"File {filepath} removed successfully.")
    else:
        print(f"File {filepath} does not exist.")

def generate_audio_file(sentence, file_name_no_ext):
    """
    Generate audio file from the given sentence.
    sentence: str
        the sentence to generate audio from
    file_name_no_ext: str
        name of the file without extension

        Returns:
        str: the path to the generated audio file.
        None if TTS is off or the sentence is empty.

    """

    print("generate...")

    if not get_config("TTS_ON", False):
        return None

    if live2d:
        sentence = live2d.remove_expression_from_string(sentence)

    if sentence.strip() == "":
        return None

    return tts.generate_audio(sentence, file_name_no_ext=file_name_no_ext)

def stream_audio_file(vc, sentence, filename):
    """
    Stream the audio file to the frontend and wait for the audio to finish. The audio and the data to control the mouth movement will be sent to the live2d frontend.

    sentence: str
        the sentence to speak
    filename: str
        the path of the audio file to stream
    """
    print("stream...")

    if not live2d:
        tts.speak_local(vc, sentence)
        return

    expression_list = live2d.get_expression_list(sentence)

    if live2d.remove_expression_from_string(sentence).strip() == "":
        live2d.send_expressions_str(sentence, send_delay=0)
        live2d.send_text(sentence)
        return


    stream_audio.StreamAudio(
        filename,
        display_text=sentence,
        expression_list=expression_list,
        base_url=live2d.base_url,
    ).send_audio_with_volume(wait_for_audio=True)

    if os.path.exists(filename):
        os.remove(filename)
        print(f"File {filename} removed successfully.")
    else:
        print(f"File {filename} does not exist.")

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
        In_Voice = True
        await channel.connect()
        await ctx.send(f'Joined {channel}')
    else:
        await ctx.send("You are not connected to a voice channel.")
#leave voice channel
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        In_voice = False
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
speech2text, tts = init_speech_services()
bot.run(TOKEN)
