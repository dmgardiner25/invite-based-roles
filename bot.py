# bot.py
import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = 'Nzg0NTc5NTIzMTMxMjExNzg3.X8rWnw.bev5AUV6UJsbTvAv4p83ib8_0l0' #os.environ['DISCORD_TOKEN']
#SERVER = 'Bot Test Server' #os.environ['DISCORD_SERVER']

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)
invites = {}
roles = {}

@bot.command(name="invite")
async def create_invite(ctx, role: str = None):
    """Create instant invite"""
    link = await ctx.channel.create_invite()
    linkStr = str(link)
    inviteCode = linkStr[linkStr.rindex('/')+1:]
    if (role != None):
        print(f'FOUND ROLE {role}')
        roles[inviteCode] = role
    await ctx.channel.send("Here is an instant invite to your server: " + linkStr)

@bot.command(name="assign")
async def assign_invite_to_role(ctx):
    """Create instant invite"""
    link = await ctx.channel.create_invite()
    await ctx.channel.send("Here is an instant invite to your server: " + str(link))

@bot.command(name="ping")
async def some_crazy_function_name(ctx):
	await ctx.channel.send("pong")

@bot.event
async def on_ready(): 
    # Getting all the guilds our bot is in
    for guild in bot.guilds:
        # Adding each guild's invites to our dict
        invites[guild.id] = await guild.invites()
        print(f'Guild: {guild}')
        print(invites[guild.id])

@bot.event
async def on_member_join(member):

    # Getting the invites before the user joining
    # from our cache for this specific guild

    invites_before_join = invites[member.guild.id]

    # Getting the invites after the user joining
    # so we can compare it with the first one, and
    # see which invite uses number increased
    invites_after_join = await member.guild.invites()

    # Loops for each invite we have for the guild
    # the user joined.
    for invite in invites_before_join:

        # Now, we're using the function we created just
        # before to check which invite count is bigger
        # than it was before the user joined.
        if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
            
            # Now that we found which link was used,
            # we will print a couple things in our console:
            # the name, invite code used the the person
            # who created the invite code, or the inviter.
            print(f"Member {member.name} Joined")
            print(f"Invite Code: {invite.code}")
            print(f"Inviter: {invite.inviter}")

            if (invite.code in roles):
                print(f'Found role')
                role = get(member.guild.roles, name='test')
                print(role.name)
                await member.add_roles(role)

            
            # We will now update our cache so it's ready
            # for the next user that joins the guild
            invites[member.guild.id] = invites_after_join
            
            # We return here since we already found which 
            # one was used and there is no point in
            # looping when we already got what we wanted
            return

@bot.event
async def on_member_remove(member):
    
    # Updates the cache when a user leaves to make sure
    # everything is up to date
    invites[member.guild.id] = await member.guild.invites()

def find_invite_by_code(invite_list, code):
    
    # Simply looping through each invite in an
    # invite list which we will get using guild.invites()
    for inv in invite_list:
        
        # Check if the invite code in this element
        # of the list is the one we're looking for
        if inv.code == code:
            
            # If it is, we return it.
            return inv

bot.run(TOKEN)
