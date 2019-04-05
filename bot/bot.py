# Main Imports
import discord
import tweepy
import youtube_dl
import extensions
import modules
import asyncio
import pyjokes
import datetime
import os
import json
import requests
import random


# Secondary Imports
from discord.ext import commands
from discord.utils import get
from modules.universal import variables
from modules.settings import settings
from modules import error_handler
from modules import prizes

# Variables
token = variables.token
players = {}
uptime = 0
version = "1.2.0.0"
lasttweet = ""
patch_notes = f"""
PATCH NOTES:
version {version}
`[ + ] Added a brand spanking new money system`
	Rob bank?
	Loot boxes?
	I think yea man. 
`[ + ] Added more error handlers`
`[ + ] Added new prizes`
`[ + ] Updated the command list on Github, finally`
"""


client = commands.Bot(command_prefix="!")
client.remove_command('help')
extensions = ['raffle', 'basic', 'roles', 'music', 'money']


async def count_down():
	global uptime
	uptime = 0
	while 1:
		await asyncio.sleep(1)
		uptime += 1


async def error_create(error, ctx):
	embed = discord.Embed(title="ERROR", description=error, colour=discord.Colour.red())
	await client.send_message(ctx.message.channel, embed=embed)
	await client.add_reaction(ctx.message, emoji="⛔")


async def message_create(msg, ctx, color, title=None):
	if title:
		embed = discord.Embed(title=title, description=msg, colour=color)
	else:
		embed = discord.Embed(title="M3-18", description=msg, colour=color)
	await client.send_message(ctx.message.channel, embed=embed)
	await client.add_reaction(ctx.message, emoji="✅")



async def permission(roles, perm):
	if perm == 1:
		return True
	elif perm == 2:
		if settings.roles[0] not in roles:
			return True
		else:
			return False
	elif perm == 3:
		if settings.roles[0] not in roles and settings.roles[1] not in roles:
			return True
		else:
			return False
	elif perm == 4:
		if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles:
			return True
		else:
			return False
	elif perm == 5:
		if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and settings.roles[3] not in roles:
			return True
		else:
			return False
	elif perm == 6:
		if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and settings.roles[3] not in roles and settings.roles[4] not in roles:
			return True
		else:
			return False
	elif perm == 7:
		if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and settings.roles[3] not in roles and settings.roles[4] not in roles and settings.roles[5] not in roles:
			return True
		else:
			return False
	elif perm == 8:
		if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and settings.roles[3] not in roles and settings.roles[4] not in roles and settings.roles[5] not in roles and settings.roles[6] not in roles:
			return True
		else:
			return False
	elif perm == 9:
		if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and \
			settings.roles[3] not in roles and settings.roles[4] not in roles and settings.roles[5] not in roles and \
			settings.roles[6] not in roles and settings.roles[7] not in roles:
			return True
		else:
			return False



async def dm_check(ctx):
	if ctx.message.channel.is_private:
		return True
	else:
		return False

async def get_tweet():
	await client.wait_until_ready()
	while not client.is_closed:
			await asyncio.sleep(2)
			global lasttweet
			if settings.swtorUpdates:
				try:
					auth = tweepy.OAuthHandler(variables.conkey, variables.consec)  # Consumer Key, Consumer Secret
					auth.set_access_token(variables.tokkey, variables.toksec)  # Token key, Token Secret
					api = tweepy.API(auth)  # logs into @Natebot01
					tweet = api.user_timeline("TORCalendar", count=1)
					tweet = tweet[0]  # Gets 50 tweets from user's timeline
					if tweet.text != lasttweet and "Event" in tweet.text:
						lasttweet = tweet.text
						tweet = tweet.text.split(" ")
						tweet.remove(tweet[-1])
						tweet.remove(tweet[0])
						tweet.remove(tweet[0])
						tweet.remove(tweet[0])
						tweet = " ".join(tweet)
						embed = discord.Embed(title = "Star Wars the Old Republic Update", description = tweet,colour = discord.Colour.blue())
						await client.send_message(client.get_channel(settings.swtorUpdateChannel), "A new Star Wars the Old Republic update"
						                                                                           " has been recieved. http://www.swtor.com/eternal-throne/updates", embed=embed)
						print("Updating discord: " + tweet)
						await client.change_presence(game=discord.Game(name=tweet))
				except Exception as e:
					print(repr(e))
				await asyncio.sleep(10)

@client.event
async def on_ready():
	print("The bot is now running.")


@client.event
async def on_member_join(member):
	channel = client.get_channel("559436932397006869")
	await message_create(f"Analyzing new member. Name: {member.mention}, Species: Human", channel, discord.Colour.teal())
	if settings.defaultRole:
		role = get(member.server.roles, name = settings.role)
		if role:
			await client.add_role(member, role)
		else:
			channel = client.get_channel("203726041456443393")
			await error_create(f"There was an error adding the default role to {member.name}", channel)
	if settings.changeUsernames:
		await message_create("Greetings. I am M3-18, a chat stimulation droid. I'm attempting to verify your account. " +
		                          "What's the name of your main character?", member, discord.Colour.light_grey())
		username = await client.wait_for_message(timeout=432000, author=member)
		role = get(member.server.roles, role="unverified")
		await client.add_role(member, role)
		if settings.usernamesAreRoles:
			await client.create_role(name=username.content, colour=discord.Colour(0xE49AB0))
			role = get(member.server.roles, role=username.content)
			if role:
				await client.add_role(member, role)
				await client.send_typing(member)
				role = get(member.server.roles, role="verified")
				await client.add_role(member, role)
				role = get(member.server.roles, role="unverified")
				await client.remove_role(member, role)
				await asyncio.sleep(2)
				await message_create(f"Your account has now been verified and activated. Welcome {username.content}.",
				                     member, discord.Colour.green())
		else:
			await client.change_nickname(member, username.content) # else, edit the users name
			await client.send_typing(member)
			role = get(member.server.roles, role="verified")
			await client.add_role(member, role)
			role = get(member.server.roles, role="unverified")
			await client.remove_role(member, role)
			await asyncio.sleep(2)
			await message_create(f"Your account has now been verified and activated. Welcome {username.content}.",
			                     member, discord.Colour.green())


@client.event
async def on_error(error, *args, **kwargs):
	await error_handler.error_report(error, "M3-18")

#@client.event
#async def on_command_error(error, ctx):
#	await error_create("That command did not process correctly. Try again.", ctx)

@client.command(pass_context=True)
async def info(ctx):
	await message_create(
		f"Thanks for asking about me {ctx.message.author.mention}! I was created by Ruko and am currently running version {version} for {uptime} seconds.", ctx,
		discord.Colour.gold())

@client.command(pass_context=True)
async def uptime(ctx):
	await message_create(f"I've been online for {uptime} and am on version {version}.", ctx, discord.Colour.purple())

@client.command(pass_context=True)
async def notes(ctx):
	await message_create("Thanks for asking. No one ever asks. Messaging them to you now.", ctx, discord.Colour.purple(), title="True Love? <3")
	await client.send_message(ctx.message.author, patch_notes)

@client.command(pass_context=True)
async def private(ctx):
	role = get(ctx.message.author.roles, name='private')
	if not await dm_check(ctx) and not role:
		role = get(ctx.message.server.roles, name="private")
		await client.add_roles(ctx.message.author, role)
		await message_create("Private channel established, " + ctx.message.author.mention, ctx, discord.Colour.light_grey())
	else:
		role = get(ctx.message.author.roles, name='private')
		if not role:
			await error_create("There has been an error with that. Use !bug to report a bug.", ctx)
		else:
			await client.remove_roles(ctx.message.author, role)
			await message_create("Private channel removed, " + ctx.message.author.mention, ctx, discord.Colour.light_grey())


@client.command(pass_context=True)
async def allow(ctx, item):
	if not await dm_check(ctx) and await permission(ctx.message.author.roles, 9):
		set = ", ".join(settings.editableSettings)
		if item == "changeUsernames":
			settings.changeUsernames = True
		elif item == "usernamesAreRoles":
			settings.usernamesAreRoles = True
		elif item == "allowCommands":
			settings.allowCommands = True
		elif item == "swtorUpdates":
			settings.swtorUpdates = True
		elif item == "levelSystem":
			settings.levelSystem = True
		elif item == "raffle":
			settings.raffle = True
		else:
			await error_create(f"{item} is not a valid settings.", ctx)
			await message_create(f"Here is a list of editable settings. {set}", ctx, discord.Colour.green(), title="Editable Settings")
			return
		await message_create(f"{item} has been turned on.", ctx, discord.Colour.green())
	else:
		await error_create("You don't have permission to do that.", ctx)


@client.command(pass_context=True)
async def disallow(ctx, item):
	if not await dm_check(ctx) and await permission(ctx.message.author.roles, 9):
		set = ", ".join(settings.editableSettings)
		if item == "changeUsernames":
			settings.changeUsernames = False
		elif item == "usernamesAreRoles":
			settings.usernamesAreRoles = False
		elif item == "allowCommands":
			settings.allowCommands = False
		elif item == "swtorUpdates":
			settings.swtorUpdates = False
		elif item == "levelSystem":
			settings.levelSystem = False
		elif item == "raffle":
			settings.raffle = False
			variables.raffle_ongoing = False
			variables.raffle_time = 0
			variables.raffle_reason = ""
			variables.raffle_users = ["None"]
		else:
			await error_create(f"{item} is not a valid settings.", ctx)
			await message_create(f"Here is a list of editable settings. {set}", ctx, discord.Colour.green(), title="Editable Settings")
			return
		await message_create(f"{item} has been turned off.", ctx, discord.Colour.red())
	else:
		await error_create("You don't have permission to do that.", ctx)


if __name__ == "__main__":
	for extension in extensions:
#		try:
		client.load_extension(extension)
#		except Exception as error:
#			print(f"{extension} can not be loaded. {repr(error)}")

	client.loop.create_task(get_tweet())
	client.loop.create_task(count_down())
	client.run(token)