import time
import discord
from OpenShockAPI import OpenShockAPI
import json


#Functions

def set_settings(name, value):
    with open('config.json', 'r') as file:
        data = json.load(file)
    data[name] = value
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

def get_settings(name):
    with open('config.json', 'r') as file:
        data = json.load(file)
    return data[name]

def increase_score(amount):
    set_settings("score", get_settings("score") + amount)

def shock(power, duration):
    openshock = OpenShockAPI(token=(get_settings("api_token")), base_url=(get_settings("base_url")))
    shocks = [{
        "id": (get_settings("deviceid")),
        "type": "Shock",
        "intensity": power,
        "duration": duration,
        "exclusive": True
    }]
    response = openshock.control_device(shocks=shocks, custom_name="Stopfossing shocking")

def vibrate(power, duration):
    openshock = OpenShockAPI(token=(get_settings("api_token")), base_url=(get_settings("base_url")))
    shocks = [{
        "id": (get_settings("deviceid")),
        "type": "Vibrate",
        "intensity": power,
        "duration": duration,
        "exclusive": True
    }]
    response = openshock.control_device(shocks=shocks, custom_name="Stopfossing vibrating")


#Check OpenShock Connection
try:
    print("Checking Connection To OpenShock...") 
    openshock = OpenShockAPI(token=(get_settings("api_token")), base_url=(get_settings("base_url")))
    api_values = openshock.list_shockers()
    connectstate = "Connected"
except:
    connectstate = "Not Connected"

print("Connection To OpenShock: " + connectstate)
print("-----------------------------------------------------------------------------------")
#Check for correct values
if connectstate == "Not Connected":
    if (get_settings("base_url") == ""):
        print("Please palce a base url in the config.json file")
    elif (get_settings("api_token") == ""):
        print("Please palce an API Token in the config.json file")
    
else:
    if (get_settings("deviceid") == ""):
        print("No Device ID Found, printing a list of aviable devices:")
        #List aviable 
        openshock = OpenShockAPI(token=(get_settings("api_token")), base_url=(get_settings("base_url")))
        shockers = openshock.list_shockers()
        for shocker in shockers:
            print(f"Device ID: {shocker['device_id']}")
            print(f"Device Name: {shocker['device_name']}")
            print(f"Device Model: {shocker['model']}")
        print("-----------------------------------------------------------------------------------")
        print("Please palce a device ID in the config.json file")


    #Start Main

    class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged on as', self.user)

        async def on_message(self, message):
            # only respond to ourselves
            if message.author != self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')
            
            #Check if from whitelisted channels or users
            if message.channel.id in get_settings("channels") or message.author.id in get_settings("users"):
                print(f"Message from {message.author}: {message.content}")
                #Check if message from self
                if message.author == self.user:
                    for word in get_settings("harm_words"):
                        count = message.content.lower().count(word)
                        if count > 0:
                            print(f"{message.author} said a prohibited word: {message.content}")
                            increase_score((get_settings("harm_words_decrease")) * count)
                else:
                    #Check if message contains decrease score
                    for word in get_settings("decrease_words"):
                        count = message.content.lower().count(word)
                        if count > 0:
                            print(f"{message.author} said a decrease word: {message.content}")
                            increase_score((get_settings("decrease_words_increase")) * count)
                    #Check if message contains increase score
                    for word in get_settings("increase_words"):
                        count = message.content.lower().count(word)
                        if count > 0:
                            print(f"{message.author} said an increase word: {message.content}")
                            increase_score((get_settings("increase_words_decrease")) * count)


    client = MyClient()
    try:
        client.run((get_settings("discord_token")))
    except discord.errors.LoginFailure:
        print("Invalid Discord Token")