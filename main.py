import discord
import os, json, random, requests
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# TODO LIST:
# - !gen command
# - !bl command
# - !stock command
# - ...

def load_bl():
    bl = []
    with open("bl.json", 'r') as f:
        for id in json.load(f):
            bl.append(id)
        return bl

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)
    
def load_secrets():
    with open("secrets.json", "r") as f:
        return json.load(f)["exeiotkn"]

def make(acc, service):
    acc = acc.replace("\n", "")
    return requests.get(f"https://exe.io/api?api={load_secrets()}&url=https://vgen-paste.000webhostapp.com/index.php?data={acc}VGEN{service}&format=text").text

def check_stock(s):
    try:
        return len(open(f"db/{s}.txt", "r").readlines())
    except Exception as e:
        return False
    
def get_one(s):
    stock = open(f"db/{s}.txt", "r").readlines()
    if len(stock) > 0:
        acc = random.choice(stock)
        pass
    else:
        return False
    new_stock = [line for line in stock if line != acc]
    with open(f"db/{s}.txt", "w") as f:
        f.writelines(new_stock)
    return acc


@client.event
async def on_ready():
    print("🚀 VGen is ready !") 

@client.command()
async def gen(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("❌ This command was disabled in dms bozo")
    else:
        if ctx.author.id in load_bl():
            await ctx.send("❌ You have been blacklisted bozo")
        else:
            if not check_stock(ctx.message.content.replace("!gen ", "")):
                await ctx.send("❌ This service look like being out of stock...")
            else:
                await ctx.send("✅ The account was sent in your dms !")
                if load_config()["is_exe"]:
                    await ctx.author.send(f"**⭐ Your {ctx.message.content.replace('!gen ', '')} account is ready !**\n\n🔗 **{make(get_one(ctx.message.content.replace('!gen ', '')), ctx.message.content.replace('!gen ', ''))}**")
                else:
                    await ctx.author.send(f"**⭐ Your {ctx.message.content.replace('!gen ', '')} account is ready !**\n\n🔗 **https://vgen-paste.000webhostapp.com/index.php?data={get_one(ctx.message.content.replace('!gen ', ''))}VGEN{ctx.message.content.replace('!gen ', '')}**")

@client.command()
async def bl(ctx):
    if ctx.author.id != load_config()["owner"]:
        pass
    else:
        try:
            user = ctx.message.content.split(" ")[1]
        except:
            await ctx.send("❌ User id is needed !")
        with open("bl.json", "r") as f:
            data = json.load(f)
            data[user] = int(user)
            open("bl.json", "w").write(str(json.dumps(data)))
        await ctx.send("✅ User was added to blacklist")

@client.command()
async def stock(ctx):
    embed = discord.Embed(title="📦 **Accounts Stock**", description="")
    for s in os.listdir("db"):
        with open(f"db/{s}") as f:
            amount = len(f.read().splitlines())
            name = (s[0].upper() + s[1:].lower()).replace(".txt","")
            embed.description += f"**{name}** ➡ {amount}\n"
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    if ctx.author.id == load_config()["owner"]:
        user = ctx.author
        await ctx.send("✅ Help message sent in your dms")
        embed = discord.Embed(title="🔎 **Help command**", description="```🧬 !gen <service> - Generate any account```\n\n```💀 !bl <userid> - Blacklist someone```\n\n```🚀 !stock - Get the actual stock```")
        await user.send(embed=embed)
    else:
        embed = discord.Embed(title="🔎 **Help command**", description="```🧬 !gen <service> - Generate any account```\n\n```🚀 !stock - Get the actual stock```")
        await ctx.send(embed=embed)

client.run(load_config()["token"])