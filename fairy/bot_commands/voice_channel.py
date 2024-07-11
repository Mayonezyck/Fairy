#join voice channel
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        In_Voice = True
        voice_client = await channel.connect()
        await ctx.channel.send(f'Joined {channel}')
        return voice_client
    else:
        await ctx.channel.send("You are not connected to a voice channel.")
        return None

#leave voice channel
async def leave(vc, ctx):
    if vc:
        await vc.disconnect()
        In_voice = False
        await ctx.channel.send("Disconnected from the voice channel.")
        return True
    else:
        await ctx.channel.send("I am not in a voice channel.")
        return False

#stream audio
'''def stream_audio_file(vc, sentence, filename):
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
'''
