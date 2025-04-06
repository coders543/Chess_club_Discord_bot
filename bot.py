
from typing import Final
import os
from random import choice
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from discord.ext import commands
from discord import app_commands
import json
# step 0 Load the token from somewhere safe
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # retrieves the token API token is really sensitive
id = os.getenv("GUILD_ID") # sensitive guild id
POLL_FILE = "polls.json" # creates a json poll file for backend data
class Client(commands.Bot):
    async def on_ready(self): # on_ready is a specific function
        print(f'{self.user} is on here') # this is where the bot is working using async
        try: # try this or run execption
            guild = discord.Object(id=id)
            synced = await self.tree.sync(guild=guild) # sync guild id to discord
            print(f"Synced {len(synced)} commands to {guild.id}")
        except Exception as e:
            print(f'Error syncing commands {e}') # shows us execption


    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}') # author is us and content is the text
        if message.author == self.user: # makes sure bot does not reply to itself self=bot message.author=us
            return
        if message.content.startswith("hello"):
            await message.channel.send(f'hi there {message.author}') # this is the bot's response
        if message.content.startswith("bye"):
            await message.channel.send(f"bye there {message.author}")
    async def on_reaction_add(self,reaction,user): # called events
        await reaction.message.channel.send("You reacted") # when we react to our own message
    # an event is hen something happens on the server
# we are going to add slash commands
intents = discord.Intents.default() # a kind of permissions
intents.message_content = True
client = Client(command_prefix="!",intents=intents) # using the Client class use the prefix ! to trigger command we do not need this btw
GUILD_ID = discord.Object(id=id) # tells the bot to run on this guild or serer
@client.tree.command(name="hello",description="this is a hello command",guild=GUILD_ID) # refer to the client object research "@" this symbol
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hi there") # respond to slash command
@client.tree.command(name="anything",description="this performs whatever you want",guild=GUILD_ID) # refer to the client object research "@" this symbol
async def say_anything(interaction: discord.Interaction, input: str): # passed a str parameter
    await interaction.response.send_message(f"hi i just said {input} like you asked")
#embeds
@client.tree.command(name="embed",description="embeded demo!",guild=GUILD_ID) # refer to the client object research "@" this symbol
async def embedded(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a title",url="https://www.google.com/",description="I am a description",color=discord.Color.red()) # red strip on the side of the embed
    embed.add_field(name="Field 1",value="Lol",inline=True) # add field inline is if you want multiple fields on same line
    #embed.set_thumbnail(url="",) creates thumbnai
    #embed.set_footer(text="hi")
    #embed.set_author()
    await interaction.response.send_message(embed=embed)
@client.tree.command(name="poll",description="First poll demo", guild=GUILD_ID)
async def poll(interaction: discord.Interaction,choice1: str, choice2: str, choice3: str, choice4: str):
    embed = discord.Embed(title="📊 Who is this?",color= discord.Color.green())
    embed.add_field(name=":one: "+ choice1,value="",inline=False) # value is required
    embed.add_field(name=":two: " +choice2,value="",inline=False)
    embed.add_field(name=":three: "+ choice3,value="",inline=False)
    embed.add_field(name=":four: " + choice4,value="",inline=False)
    embed.set_footer(text="Please choose 1 of the 4 icons and react! ")
    #embed.set_footer(text="hi") footer gives messages at the end
    #embed.set_author(name="Who is this?") this code is at the really top

    message = await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()  # Get message object
    # Add reactions
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    responses = {"️1️⃣":0,"2️⃣":0,"3️⃣":0,"4️⃣":0}
    if await message.add_reaction("1️⃣"):
        responses["1️⃣"] += 1 # accesses value pair
    elif await message.add_reaction("2️⃣"):
        responses["2️⃣"] += 1
    elif await message.add_reaction("3️⃣"):
        responses["3️⃣"] += 1
    elif await message.add_reaction("4️⃣"):
        responses["4️⃣"] += 1
    save_polls(responses)
def load_polls():
    try:
        with open(POLL_FILE, "r") as file: # open file in read mode
            data = json.load(file) # convert json -> python
            return data
    except (FileNotFoundError,json.JSONDecodeError) as e: # return an exeception if data is empty and no json data to decode
        print(f"Json sucks {e}")

def save_polls(datas):
    with open(POLL_FILE,"w") as file:
        json.dump(datas, file, indent=4) # set indent=4 for pretty printing json.dump writes to json file json.dump(obj, file, indent=4)








client.run(TOKEN)

'''
POLL_FILE = "polls.json"
# Function to Load Poll Data
def load_polls():
    if not os.path.exists(POLL_FILE):
        with open(POLL_FILE, "w") as f:
            json.dump({}, f)  # Create empty JSON file
    with open(POLL_FILE, "r") as f:
        return json.load(f)

# Function to Save Poll Data
def save_polls(polls):
    with open(POLL_FILE, "w") as f:
        json.dump(polls, f, indent=4)

# Poll command
@client.tree.command(name="poll", description="Create a poll!",guild=GUILD_ID)
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str):
    embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.green())
    embed.add_field(name="🟢 Option 1", value=option1, inline=False)
    embed.add_field(name="🔴 Option 2", value=option2, inline=False)
    embed.set_footer(text="React to vote!")

    message = await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()  # Get message object

    # Add reactions
    await message.add_reaction("🟢")
    await message.add_reaction("🔴")

    # Store poll in JSON
    polls = load_polls()
    polls[str(message.id)] = {"question": question, "option1": option1, "option2": option2, "votes": {"🟢": 0, "🔴": 0}}
    save_polls(polls)

    await interaction.followup.send(f"Poll created! React with 🟢 or 🔴 to vote.")
client.run(TOKEN) # running the bot
# JSON File Path
'''


'''
# Step 1 Bot Setup intents are permissions
intents : Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)
#Step 2 message functionality
async def send_message(message: Message,user_message: str ) -> None:
    if not user_message:
        print("Message was empty because intents were not enabled probably")
        return
    if is_private := user_message[0] == "?": # walrus operator?
        user_message = user_message[1: ]
    try:
        response: str = get_response(user_message) # this is for static tying instead of dynamic. response: str = "blah". Code now knows that response is supposed to be a str
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
# Step 3 Hand the startupt for our bot
@client.event # what is this?
async def on_ready()-> None:
    print(f"{client.user} is now running ")
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    username: str = str(message.author)
    user_message: str = (message.content)
    channel: str = str(message.channel)
    print(f'[{channel}{username} :{user_message}]')
    await send_message(message, user_message)
# Step 5 main entry point
def main()-> None:
    client.run(token=TOKEN)
if __name__ == "__main__": # what does this mean
    main()
'''