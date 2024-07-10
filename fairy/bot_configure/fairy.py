import discord
import re
import time
import datetime
from discord.ext import commands
from discord.ext import tasks
from llm.llm_factory import LLMFactory
from fairy.bot_commands import voice_channel
#from fairy.timely_task_handler import task_with_llm
import asyncio
from concurrent.futures import ThreadPoolExecutor


class Fairy(discord.Client):
    def __init__(self, testchannel, llm_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # an attribute we can access from our task
        self.testchannel = testchannel
        self.llmConnected = self.init_agent(llm_info)
        self.audio_out_enabled = False
        self.temp = None
        self.isThinking = False
        self.executor = ThreadPoolExecutor()
        self.freeChat = False
        self.freeChatChannel = None


    def init_agent(self,llm_info):
        try:
            self.llm = LLMFactory.create_llm(llm_provider=llm_info[0], SYSTEM_PROMPT=llm_info[2], **llm_info[1])
            #print(llm_info)
            return True
        except ValueError:
            print("Oops! Something is wrong")
            return False

    def shouldIgnore(self, ctx):
        if ctx.author == self.user :
            return True
        if ctx.channel != self.freeChatChannel and ctx.channel.id != self.testchannel:
            return True
        return False


    def coolDown(self):
        self.temp = None
        self.isThinking = False

    def checkCommand(self, message):
        cleaned_message = re.sub(r'<@!?[0-9]+>', '', message.content).strip()
        if(cleaned_message[0] == '!'):
            print(cleaned_message[1:7])
            if cleaned_message[1:7] == 'enable':
                self.enableFreeChat(message.channel)
                return True
            elif cleaned_message[1:8] == 'disable':
                self.disableFreeChat()
                return True
        return False

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        self.my_background_task.start()

    def justEcho(self, message):
        cleaned_message = re.sub(r'<@!?[0-9]+>', '', message.content).strip()
        response = f"Bot was mentioned! Message: {cleaned_message}"
        return response

    def enableFreeChat(self, channel):
        self.freeChatChannel = channel
        self.freeChat = True

    def disableFreeChat(self):
        self.freeChatChannel = None
        self.freeChat = False

    async def typeToOutput(self, message):
        if not self.llmConnected:
            response = 'Bro, you need to check the LLM module, why there\'s no error??'
            await message.reply(response)
        elif self.isThinking:
            response = f'Sorry, {message.author} I am busy right now. I will come back to you later <3'
            await message.reply(response)
        else:
            #await self.askLLM(message)
            await message.channel.typing()
            await self.run_in_executor(message)
            #while self.isThinking:
                #print('...')
                #await message.channel.typing()
        #await message.channel.typing()
            await message.channel.typing()
            await message.reply(self.temp)
            self.coolDown()

    async def sayToOutput(self, message):
        pass #TODO-WASS

    def askLLM(self, message):
        cleaned_message = re.sub(r'<@!?[0-9]+>', '', message.content).strip()
        #await message.channel.send(f'{self.isThinking, self.temp}')
        author = message.author
        wrapped_message = f'{author}:{cleaned_message}'
        self.temp = self.llm.chat(wrapped_message)
        self.isThinking = False
        #time.sleep(2)
        #self.temp = None

    async def run_in_executor(self, message):
        self.isThinking = True
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(self.executor, self.askLLM, message)
        return result

    async def chat(self, message):
        if self.audio_out_enabled:
            await self.sayToOutput(message)
        else:
            await self.typeToOutput(message)

    async def on_mentioned(self, message):
        if not self.checkCommand(message):
            await self.chat(message)

                # if In_Voice:
        #     if message.author.voice:
        #         voice_channel = message.author.voice.channel
        #         await getResponse_audio(llm, voice_channel, cleaned_message)
        #     else:
        #         await message.channel.send('How can you listen if you are not in a voice channel?')
        # else:
        #     llmresponse = await getResponse(llm, cleaned_message)
        #     await message.channel.send(llmresponse)

    # Event that triggers on new message
    async def on_message(self,message):
        if self.shouldIgnore(message):return
        #await DEBUG_printMessageInfo(message)
        if self.user.mentioned_in(message):
            await self.on_mentioned(message)
        elif self.freeChat and message.channel == self.freeChatChannel:
            await self.chat(message)

        #await commands.Bot.process_commands(message)

    #-----------------------------Tested Commands----------------------

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(self.testchannel)   # channel ID goes here
        await channel.send(datetime.datetime.now())

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


    #-----DEPRECATED----
    '''@commands.command('join')
    async def join_voice(self,ctx):
        print('???')
        await voice_channel.join(ctx)
    @commands.command('leave')
    async def leave_voice(self,ctx):
        await voice_channel.leave(ctx)'''
