import string
alphabet_list = list(string.ascii_lowercase)

def sumstring(x):
    display=''
    for i in range(0,len(x)):
        display+=x[i]
    return display

def word_to_num(a):
    a_change=''
    for i in a:
        try:
            i = str(int(i))
            a_change+=i
        except:
            i=str(alphabet_list.index(i)+1)
            a_change+=i
    return int(a_change)

def encrypt(letter,step):
    letter_list=list(letter)
    for i in range(0,len(letter_list)):
        if letter_list[i] in alphabet_list:
            position=alphabet_list.index(letter_list[i])
            new_position=(position+step)%len(alphabet_list)
            letter_list[i]=alphabet_list[new_position]
    return sumstring(letter_list)




async def encrypt_decrypt(message,client):
    ## Welcome message
    bot_response=await message.channel.send('''Welcome to 'YoYo Cipher' DeEnCryptor using YoYoAlgorithm
                                
Do you want to "Decrypt" or "Encrpyt"''')
    ## response1
    response1 = await client.wait_for("message")
    # ignore others
    while not response1.author==message.author:
        response1 = await client.wait_for("message")

    ### Encrypt
    if response1.content.lower()=='encrypt' or response1.content.lower()=='e':
                await bot_response.edit(content="Welcome to 'YoYo Cipher' DeEnCryptor using YoYoAlgorithm")
                await response1.delete()
                bot_response = await message.channel.send('Type message you want to encrypt', delete_after = 20)

                ##response2
                response2 = await client.wait_for("message")
                while not response2.author==message.author: #ignore others
                    response2 = await client.wait_for("message")
                message_to_encrypt=response2.content.lower()
                await response2.delete() #delete message to encrypt
                await bot_response.delete() #delete bot message

                bot_response = await message.channel.send('Create a Key(Password)')

                ##response3
                response3 = await client.wait_for("message")
                while not response3.author==message.author: #ignore others
                    response3 = await client.wait_for("message")
                
                key=word_to_num(response3.content.lower().replace(' ', ''))

                await response3.delete() #delete key
                await bot_response.delete() #delete bot message

                #send the encrypted message
                await message.channel.send(f'Encrypted message : {encrypt(letter = message_to_encrypt , step = key)}')

    ### Decrypt
    if response1.content.lower()=='decrypt' or response1.content.lower()=='d':
                await bot_response.edit(content="Welcome to 'YoYo Cipher' DeEnCryptor using YoYoAlgorithm")
                await response1.delete()
                bot_response = await message.channel.send('Type message you want to Decrypt')

                ##response2
                response2 = await client.wait_for("message")
                while not response2.author==message.author: #ignore others
                    response2 = await client.wait_for("message")
                message_to_decrypt=response2.content.lower()
                await response2.delete() #delete message to decrypt
                await bot_response.delete() #delete bot message

                bot_response = await message.channel.send('Create a Key(Password)')

                ##response3
                response3 = await client.wait_for("message")
                while not response3.author==message.author: #ignore others
                    response3 = await client.wait_for("message")
                
                key=word_to_num(response3.content.lower().replace(' ', ''))

                await response3.delete() #delete key
                await bot_response.delete() #delete bot message

                #send the decrypted message
                await message.channel.send(f'Encrypted message : {encrypt(letter = message_to_decrypt , step = -key)}', delete_after=10)




