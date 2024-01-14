import random
import asyncio

def sumstring(k):
    m=''
    for x in k:
        m+=x+' '
    return m

async def wordguess(message,client):

    ### Setup
    lifespan = 5
    life = lifespan

    word_library ={
    'animals':[
        "Giraffe",
        "Crocodile",
        "Beetle",
        "Butterfly",
        "Chicken",
        "Dolphin",
        "Hamster"
        "Tiger",
        "Panda",
        "Horse",
        "Gecko",
        "Zebra",
        "Eagle",
        "Rhino",
        "Sheep",
        "Shark",
        "Cheetah",
        "Mouse",
        "Camel",
        "panda",
        "elephant"]
    }

    # Select the word
    word_book=word_library['animals']
    selected_word = word_book[random.randint(0,len(word_book)-1)].lower()

    # List for display letters
    sub_display=[]
    for i in range(0,len(selected_word)):
        sub_display.append('_')

    await message.channel.send('''Welcome to Wordguess game
hint: Animals''')

    ## Display First UI
    display=await message.channel.send(f'''```
YoYo WordGuess
YoYo WordGuess
YoYo WordGuess
YoYo WordGuess
YoYo WordGuess
```''')
    
    await asyncio.sleep(1.5) #Delay
    
    ###### Gamplay Loop
    while life>=0:
        ## Main display
        await display.edit(content=f'''```You have {life*"♡ "} hearts left
{4*len(sub_display)*'_'}

    {sumstring(sub_display).upper()}
{4*len(sub_display)*'_'}```''')
        
        ## Input player answer
        guess=await client.wait_for('message')
        while not message.channel==guess.channel:
            guess=await client.wait_for('message')

        is_correct=False
        ## Reaveal by changing sub_display
        for i in range(0,len(selected_word)):
            if guess.content.lower()==selected_word[i]:
                sub_display[i]=selected_word[i]
                is_correct=True

        ## React Correct or Incorrect
        if is_correct:
            #react
            await guess.add_reaction("✅")
            await asyncio.sleep(0.5)
            await guess.delete()
        elif not is_correct:
            #react
            await guess.add_reaction("❌")
            life-=1
        
        ### Final result
        ## WIN
        if sumstring(sub_display).replace(" ", "").lower()==selected_word:
            #send win message
            await message.channel.send(f'''```YOU W I N
YOU W I N
YOU W I N
{4*len(sub_display)*'_'}

{sumstring(sub_display).upper()}
{4*len(sub_display)*'_'}
MVP : {guess.author.nick}```''')
            break

        ## Lose
        elif life==0:
            await display.edit(content=f'''```You have no hearts left
    {4*len(sub_display)*'_'}

        {sumstring(sub_display).upper()}
    {4*len(sub_display)*'_'}```''')
            
            await message.channel.send('YOU L O S E')
            await asyncio.sleep(5)
            await message.channel.send(f"The correct word is '{selected_word.capitalize()}'")