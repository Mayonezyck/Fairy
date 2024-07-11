#join voice channel
import azure.cognitiveservices.speech as speechsdk
import os
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

async def playAudio(vc, audioPath ,ctx):
    import discord
    if vc:
        # Play the local file test.mp3
        source = discord.FFmpegPCMAudio(audioPath)
        vc.play(source)
        await ctx.channel.send(f"Playing {audioPath}")
    else:
        await ctx.channel.send("You are not connected to a voice channel.")

async def text_to_speech(text):
    speech_key = "01d8f92bbf8c460a9d65ea412fbf3e4f"
    service_region = "westus2"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

    temp_dir = ".temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    temp_audio_file_name = os.path.join(temp_dir, "temp_audio.mp3")
    audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_audio_file_name)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return temp_audio_file_name
    else:
        raise Exception("Speech synthesis failed")

async def after_play(vc, filename):
    while vc.is_playing():
        pass
    if os.path.exists(filename):
        os.remove(filename)
        print(f'Temporary file {filename} deleted.')



if __name__ == "__main__":
    print(text_to_speech('hello world'))

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
