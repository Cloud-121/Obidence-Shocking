#Made by Cloud (aka Scarlett) to have fun with myself :3
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
    try:
        openshock = OpenShockAPI(token=(get_settings("api_token")), base_url=(get_settings("base_url")))
        shocks = [{
            "id": (get_settings("deviceid")),
            "type": "Shock",
            "intensity": power,
            "duration": duration,
            "exclusive": True
        }]
        print(f"Shocking with power: {power}, duration: {duration}")
        response = openshock.control_device(shocks=shocks, custom_name="Stopfossing_shocking")
    except Exception as e:
        print("OpenShock Connection Failed")
        print(e)
    

def vibrate(power, duration):
    try:
        openshock = OpenShockAPI(token=(get_settings("api_token")), base_url=(get_settings("base_url")))
        shocks = [{
            "id": (get_settings("deviceid")),
            "type": "Vibrate",
            "intensity": power,
            "duration": duration,
            "exclusive": True
        }]
        print(f"Vibrating with power: {power}, duration: {duration}")
        response = openshock.control_device(shocks=shocks, custom_name="Stopfossing_vibrating")
    except Exception as e:
        print("OpenShock Connection Failed")
        print(e)


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
            if message.channel.id in get_settings("discord_channels") or message.author.id in get_settings("always_allowed_users"):
                print(f"Message from {message.author}: {message.content}")
                #Check if message from self
                if message.author == self.user:
                    for word in get_settings("harm_words"):
                        count = message.content.lower().count(word)
                        if count > 0:
                            print(f"{message.author} said a prohibited word: {message.content}")
                            increase_score((get_settings("harm_words_decrease")) * count)
                            print(f"Score: {get_settings('score')}")

                    #Check if message needs vibration
                    if (get_settings("score")) >= 100 and (get_settings("score")) <= 200:
                        print(f"Score above 100, Preforming calculations")
                        score = get_settings("score")
                        percent = ((score - 100) / 100) * 100
                        vibrate(percent, 1)
                    #Check if message needs shocking
                    elif (get_settings("score")) > 200:
                        print(f"Score above 200, Performing calculations")
                        score = get_settings("score")
                        duration = ((score - 200) / 800) * 30
                        percent = ((score - 200) / 800) * 100
                        shock(percent, duration)

                else:
                    if message.mentions and message.mentions[0].id == self.user.id or message.reference and message.reference.resolved and message.reference.resolved.author.id == self.user.id:
                        #Check if message contains decrease score
                        for word in get_settings("decrease_words"):
                            count = message.content.lower().count(word)
                            if count > 0:
                                print(f"{message.author} said a decrease word: {message.content}")
                                increase_score((get_settings("decrease_words_increase")) * count)
                                print(f"Score: {get_settings('score')}")
                        #Check if message contains increase score
                        for word in get_settings("increase_words"):
                            count = message.content.lower().count(word)
                            if count > 0:
                                print(f"{message.author} said an increase word: {message.content}")
                                increase_score((get_settings("increase_words_decrease")) * count)
                                print(f"Score: {get_settings('score')}")


    client = MyClient()
    try:
        client.run((get_settings("discord_token")))
    except discord.errors.LoginFailure:
        print("Invalid Discord Token")