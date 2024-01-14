from keep_alive import keep_alive
try:
    keep_alive()
    run_on_server=True
except:
    run_on_server=False
version='2.0'

from io import StringIO
import discord
from yoyo_wordguess import wordguess
from yoyo_cipher import encrypt_decrypt
from prompt_books import prompt_dictionary

#<Message id=1181988154081820802
# channel=<TextChannel id=1180815101285126194 name='pyyobot-lab' position=6 nsfw=False news=False category_id=441226721815953411>
# type=<MessageType.default: 0>
# author=<Member id=508135966612127766 name='nostradamus6591' global_name='Nostradamus' bot=False nick='นอสตราดามุส'
# guild=<Guild id=441226721815953409 name='INJUSTICE LAND แดนคนเหลี่ยม' shard_id=0 chunked=False member_count=103>>
# flags=<MessageFlags value=0>>#

#-----------------------------------Code Setup---------------------------------

#Time
import datetime
from datetime import timezone
# GMT+7
current_datetime = datetime.datetime.now(timezone(datetime.timedelta(hours=7)))
#store variables
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
hour = current_datetime.hour
minute = current_datetime.minute
second = current_datetime.second

#PaLM API
import google.generativeai as genai
genai.configure(api_key='AIzaSyAIed4JR--ZyQU4rdJA1kWVNq97Lj-Ab34')
model = genai.GenerativeModel('gemini-pro')
prob=genai.types.HarmProbability.HIGH
thershold=genai.types.HarmBlockThreshold.BLOCK_NONE
safety_settings = [
  {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE"
  },

  {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE"
  },

  {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_NONE"
  },

  {
      "category": "HARM_CATEGORY_DANGEROUS",
      "threshold": "BLOCK_NONE"
  },
]

#------------------------------------Bot Initial set up----------------------------------
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#---------------------------------CODE FUNCTION--------------------------------
chatful = model.start_chat(history=[])
def setup(prompt_1,prompt_2):
    global chat
    chat = model.start_chat(history=[])
    prompt =f"""For an ENTIRE conversation, you MUST be {prompt_1} You also have to response {prompt_2} within one or two sentence."""
    chat.send_message(content=prompt,safety_settings=safety_settings,generation_config=genai.types.GenerationConfig(max_output_tokens=50,temperature=0.3,top_k=40,top_p=1.0))
    #print(chat.history[1].parts)

chatfull = model.start_chat(history=[])
def setup_full(prompt_1,prompt_2):
    global chatfull
    chatfull = model.start_chat(history=[])
    prompt =f"For an ENTIRE conversation, you MUST be {prompt_1}. You also have to response {prompt_2} with no more than 2000 characters."
    chatfull.send_message(content=prompt,safety_settings=safety_settings)

#-------------------------------------------------------------------------

#Inform Bot Status to Host
@client.event
async def on_ready():
    print(f'{hour}:{minute}:{second}. {client.user} ONLINE')

############################# MESSAGE COMMAND ##############################
prompt_dict=prompt_dictionary()
prompt_1=prompt_dict['pyyoboy'][0]
prompt_2=prompt_dict['pyyoboy'][1]
setup(prompt_1,prompt_2)
setup_full(prompt_1,prompt_2)

check_log=False
count_log=0
@client.event
async def on_message(message):
    #Code Variables
    global chat
    global chatfull
    global prompt_dict
    global prompt_1
    global prompt_2
    global version
    global check_log #Check log
    global count_log #Check log
    is_harvest=False #Hooke

    # return when message from bot
    if message.author == client.user:
        return
#-----------------------------Check Bot status------------------------------------
    elif 'yoyo' and 'status' in message.content.lower():
        if run_on_server:
            await message.channel.send(f'PyyoBoy {version} is currently running on servers')
        else:
            await message.channel.send(f'PyyoBoy {version} is currently running locally (debugging)')

#-----------------------------Check Log to terminal------------------------------
    #Enabled Disabed check_log
    elif 'yoyo' and 'log' in message.content.lower():
        count_log+=1
        if not count_log%2==0:    
            check_log=True
            print('check_log is enabled')
        else:
            check_log=False
            print('check_log is disabled')
    #Trigger check_log
    elif check_log:
        print(f'{hour}:{minute}:{second} {message.guild.name} {message.author} : {message.content}')
#-----------------------------Basic---yoyo-----------------------
    #Trigger

    elif message.content.lower()=='yoyo':
            await message.channel.send(f'''
    ***Command List*** :```

    "yoyo prompt"   to see available prompts

    "yo "   ask any questions (brief response)

    "yoyo "   ask any questions (full response)  

    "yoyo clear"   to clear chat memory

    "yoyo cipher"   encrypt or decrpyt messages

    "yoyo wordguess"   playing wordguess game
    ```''')

#------------------------Hooke message----$harvest-------$delete------------
    #Trigger Hooke
    elif message.content.lower().startswith('$harvest'):
        #alert in channel
        hook=await message.channel.send('Hooking messages...')
        #setup
        message_list=[]
        is_harvest=True

    #Do the Hooke
    elif is_harvest:
        if hook.channel==message.channel:
            message_list.append(message)

    #Delete Hooked
    elif message.content.startswith('$delete'):
        while not len(message_list)==1:
            await message_list[0].delete()
            message_list.pop(0)
        is_harvest=False

#------------------------Word guesser-----------yoyo wordguess------------------
    #Trigger
    elif message.content.lower()==('yoyo wordguess'):
        await wordguess(message=message,client=client)
#----------------------------------Encrypt Decrypt---------------yoyo cipher---------------------
    #Trigger
    elif message.content.lower()=='yoyo cipher':
        await encrypt_decrypt(message=message,client=client)

#------------------------------------------------------yoyo yo------------------
    elif message.content.lower()=='yoyo prompt':
        sum_name='Available prompt :'
        for name in prompt_dict:
            sum_name+=f'''
    {name.capitalize()}'''
        await message.channel.send(f'''{sum_name}

To change these prompt, type: yoyo "your prompt"
EX: yoyo feynman''')

    elif message.content.lower()=='yoyo clear':
        await message.add_reaction("✅")
        setup(prompt_1,prompt_2)
        setup_full(prompt_1,prompt_2)

    elif message.content.lower().split()[0] == 'yoyo' and message.content.split()[1].lower() in prompt_dict:
        prompt_1=prompt_dict[message.content.lower().split()[1]][0]
        prompt_2=prompt_dict[message.content.lower().split()[1]][1]
        setup(prompt_1,prompt_2)
        setup_full(prompt_1,prompt_2)
        await message.channel.send(f'PyyoBoy is now {message.content.split()[1].capitalize()}')

    elif message.content.lower().split()[0] == 'yo':

        prompt =f"""{message.content.split(' ',1)[1]}"""
        response = chat.send_message(content=prompt,safety_settings=safety_settings,generation_config=genai.types.GenerationConfig(max_output_tokens=100,temperature=0.2,top_k=40,top_p=0.95))
        try:
            await message.channel.send(response.text)
        except:
            await message.channel.send('Error')

    elif message.content.lower().split()[0] == 'yoyo':

        prompt =f"""{message.content.split(' ',1)[1]}"""

        response = chatfull.send_message(content=prompt,safety_settings=safety_settings,generation_config=genai.types.GenerationConfig(max_output_tokens=16000,temperature=0.2,top_k=40,top_p=0.95))
        try:
            await message.channel.send(response.text)
        except:
            buffer = StringIO(response.text)
            f = discord.File(buffer, filename="pyyoboy.txt")
            await message.channel.send(file=f)
          
client.run('MTE4NTA3NzU4MjAyNzI5Njc3OA.GngXog.oH3K5wk6PHFTKI79AWYU1Ti8Z-k2GDPMJod1y8')