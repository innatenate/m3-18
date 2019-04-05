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
import bot

# Secondary Imports
from discord.ext import commands
from discord.utils import get
from modules.universal import variables
from modules.settings import settings
from modules import prizes
money_name = "credits"
money_per_message = 5
users = {}
extra_raffle_ticket = 100
bank_robbed = False
bank_robbing_fee = 100
loot_box_cost = 700

class money:
	def __init__(self, client):
		self.client = client

	async def error_create(self, error, ctx):
		client = self.client
		embed = discord.Embed(title="ERROR", description=error, colour=discord.Colour.red())
		await client.send_message(ctx.message.channel, embed=embed)
		await client.add_reaction(ctx.message, emoji="⛔")

	async def message_create(self, msg, ctx, color, title=None):
		client = self.client
		if title:
			embed = discord.Embed(title=title, description=msg, colour=color)
		else:
			embed = discord.Embed(title="M3-18", description=msg, colour=color)
		await client.send_message(ctx.message.channel, embed=embed)
		await client.add_reaction(ctx.message, emoji="✅")

	async def permission(self, roles, perm):
		client = self.client
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
			if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and \
					settings.roles[3] not in roles:
				return True
			else:
				return False
		elif perm == 6:
			if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and \
					settings.roles[3] not in roles and settings.roles[4] not in roles:
				return True
			else:
				return False
		elif perm == 7:
			if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and \
					settings.roles[3] not in roles and settings.roles[4] not in roles and settings.roles[
				5] not in roles:
				return True
			else:
				return False
		elif perm == 8:
			if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and \
					settings.roles[3] not in roles and settings.roles[4] not in roles and settings.roles[
				5] not in roles and settings.roles[6] not in roles:
				return True
			else:
				return False
		elif perm == 9:
			if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and \
					settings.roles[3] not in roles and settings.roles[4] not in roles and settings.roles[
				5] not in roles and \
					settings.roles[6] not in roles and settings.roles[7] not in roles:
				return True
			else:
				return False

	async def dm_check(self, ctx):
		client = self.client
		if ctx.message.channel.is_private:
			return True
		else:
			return False

	async def on_message(self, msg):
		if msg.author.id not in users:
			users[msg.author.id] = 0
		users[msg.author.id] += money_per_message

	@commands.command(pass_context=True)
	async def givemoney(self, ctx, mem: discord.Member=None, num=5):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 1):
			if not mem:
				await money.error_create(self, f"You have to specify a member. Optionally, you can specify an amount of {money_name}. (Default is 5)", ctx)
				return
			if not ctx.message.author.id in users:
				ValueError()
			else:
				if users[ctx.message.author.id] < 5:
					await money.error_create(self, f"You don't have enough to give. Your balance is {str(users[ctx.message.author.id])}.", ctx)
				else:
					users[ctx.message.author.id] -= num
					if mem.id not in users:
						users[mem.id] = 0
					users[mem.id] += num
					await money.message_create(self, f"You have successfully transferred {str(num)} {money_name} "
					f"to {mem.mention}. Your balance is {str(users[ctx.message.author.id])}.", ctx, discord.Colour.dark_green())
		else:
			ValueError()


	@commands.command(pass_context=True)
	async def allmoney(self, ctx):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 1):
			dis_users = self.client.get_all_members()
			mon_users = []
			for user in dis_users:
				if user.id not in users:
					users[user.id] = 0
				mon_users.append(f"**{user.name}** : {str(users[user.id])}")
			mon_users = "\n".join(mon_users)
			await money.message_create(self, str(mon_users), ctx, discord.Colour.dark_green(), title = "Member Balances")
		else:
			ValueError()


	@commands.command(pass_context=True)
	async def addmoney(self, ctx, mem: discord.Member=None, num=5):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 7):
			if not mem:
				await money.error_create(self, f"You have to specify a member. Optionally, you can specify an amount of {money_name}. (Default is 5)", ctx)
				return
			if mem.id not in users: users[mem.id] = 0
			users[mem.id] += num
			await money.message_create(self, f"You have successfully added {str(num)} {money_name} to {mem.mention}'s account.", ctx, discord.Colour.gold())
		else:
			ValueError()


	@commands.command(pass_context=True)
	async def submoney(self, ctx, mem: discord.Member = None, num=5):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 7):
			if not mem:
				await money.error_create(self,
				                         f"You have to specify a member. Optionally, you can specify an amount of {money_name}. (Default is 5)",
				                         ctx)
				return
			if mem.id not in users: users[mem.id] = 0
			users[mem.id] -= num
			await money.message_create(self, f"You have successfully taken {str(num)} {money_name} from {mem.mention}'s account.", ctx, discord.Colour.gold())
		else:
			ValueError()


	@commands.command(pass_context=True)
	async def setmoney(self, ctx, mem: discord.Member = None, num=5):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 7):
			if not mem:
				await money.error_create(self,
				                         f"You have to specify a member. Optionally, you can specify an amount of {money_name}. (Default is 0)",
				                         ctx)
				return
			users[mem.id] = num
			await money.message_create(self, f"You have successfully set {mem.mention}'s account balance to {str(num)} {money_name}.", ctx, discord.Colour.gold())
		else:
			ValueError()


	@commands.command(pass_context=True)
	async def money(self, ctx, member:discord.Member = None):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 1):
			if member:
				if member.id not in users:
					users[member.id] = 0
				await money.message_create(self, f"{member.mention} currently has a balance of {str(users[member.id])} {money_name}", ctx, discord.Colour.green())
			else:
				if ctx.message.author.id not in users:
					users[ctx.message.author.id] = 0
				await money.message_create(self, f"You currently have a balance of {str(users[ctx.message.author.id])} {money_name}", ctx, discord.Colour.green())
		else:
			ValueError()


	@commands.command(pass_context=True)
	async def balance(self, ctx, member:discord.Member = None):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 1):
			if member:
				if member.id not in users:
					users[member.id] = 0
				await money.message_create(self, f"{member.mention} currently has a balance of {str(users[member.id])} {money_name}", ctx, discord.Colour.green())
			else:
				if ctx.message.author.id not in users:
					users[ctx.message.author.id] = 0
				await money.message_create(self, f"You currently have a balance of {str(users[ctx.message.author.id])} {money_name}", ctx, discord.Colour.green())
		else:
			ValueError()


	@commands.command(pass_context=True)
	async def joinraffle(self, ctx):
		client = self.client
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, settings.rafflePerm):
			if not settings.raffle:
				await money.error_create(self, "Raffles are not currently allowed in this server.", ctx)
				return
			if not variables.raffle_ongoing:
				await money.error_create(self, "There is no ongoing raffle.", ctx)
			else:
				mem = ctx.message.author.id
				if ctx.message.author.name in variables.raffle_users:
					if mem not in users:
						users[mem] = 0
						await money.error_create(self, f"You don't have enough {money_name} to enter the raffle again. Entry cost is {str(extra_raffle_ticket)}", ctx)
						return
					elif users[mem] < extra_raffle_ticket:
						await money.error_create(self, f"You don't have enough {money_name} to enter the raffle again. Entry cost is {str(extra_raffle_ticket)}", ctx)
						return
					else:
						users[mem] -= extra_raffle_ticket
						variables.raffle_users.append(ctx.message.author.name)
						num_of_ent = 0
						for user in variables.raffle_users:
							if user == ctx.message.author.name:
								num_of_ent +=1
						await money.message_create(self, f"You have succesfully entered the raffle again. Your number of entries: {str(num_of_ent)}", ctx, discord.Colour.green())
				else:
					variables.raffle_users.append(ctx.message.author.name)
					await money.message_create(self, f"{ctx.message.author.mention} has been entered into the raffle."
					                         f" The remaining time is {str(round(variables.raffle_time / 60 / 60))} "
					                         f"hours remaining and the prize/reason is {variables.raffle_reason}.",
					                         ctx, discord.Colour.green())
		else:
			ValueError()


	@commands.command(pass_context=True)
	async def robbank(self, ctx):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 3):
			global bank_robbed
			if bank_robbed == False:
				mem = ctx.message.author.id
				if mem not in users:
					users[mem] = 0
				if users[mem] < bank_robbing_fee:
					await money.error_create(self, f"You don't have enough {money_name} to buy weapons to rob the bank. "
					f"Fee is {bank_robbing_fee} {money_name}.", ctx)
				else:
					bank_robbed = True
					await money.message_create(self, f"{ctx.message.author.mention} is robbing the bank!", ctx, discord.Colour.red())
					await asyncio.sleep(3)
					get_away_cost = random.randrange(-900,700)
					if get_away_cost < 0:
						await money.message_create(self, f"{ctx.message.author.mention} barely got out of the bank alive. "
						f"They lost {str(get_away_cost)} {money_name}.", ctx, discord.Colour.red())
						users[mem] -= get_away_cost
					else:
						await money.message_create(self, f"{ctx.message.author.mention} got out with a bag full of {money_name}!"
						f"They gained {str(get_away_cost)} {money_name}.", ctx, discord.Colour.green())
						users[mem] += get_away_cost
					await asyncio.sleep(120)
					bank_robbed=False
			else:
				await money.error_create(self, "The bank was recently robbed. Try waiting a tad longer.", ctx)


	@commands.command(pass_context=True)
	async def lootbox(self, ctx):
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 4):
			mem = ctx.message.author.id
			if mem not in users:
				users[mem] = 0
			if users[mem] < loot_box_cost:
				await money.error_create(self, f"You don't have enough {money_name} to buy a blackmarket loot box. "
				f"Cost is {loot_box_cost} {money_name}.", ctx)
			else:
				users[mem] -= loot_box_cost
				choice = prizes.prizes[random.randrange(len(prizes.prizes))]
				num = 0
				for prize in prizes.prizes:
					if prize == choice:
						num += 1
				chance = num/len(prizes.prizes) * 100.0
				await money.message_create(self, f"{ctx.message.author.mention} has won {choice}. "
				f"The chances of winning {choice} were {str(round(chance))}%.", ctx, discord.Colour.gold(), "Congratulations!")
				await self.client.send_message(ctx.message.author, f"Congrats on winning {choice}. To claim your price, message your guildleader!")



	@commands.command(pass_context=True)
	async def changemoneyname(self, ctx, money="credits"):
		global money_name
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 9):
			money_name = money
		else:
			await money.error_create(self, "You don't have enough permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def moneypermessage(self, ctx, money=0):
		global money_per_message
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 9):
			money_per_message = money
		else:
			await money.error_create(self, "You don't have enough permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def extrarafflecost(self, ctx, money=0):
		global extra_raffle_ticket
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 9):
			extra_raffle_ticket = money
		else:
			await money.error_create(self, "You don't have enough permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def bankrobfee(self, ctx, money=0):
		global bank_robbing_fee
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 9):
			bank_robbing_fee = money
		else:
			await money.error_create(self, "You don't have enough permission to do that.", ctx)

	@commands.command(pass_context=True)
	async def lootboxfee(self, ctx, money=0):
		global loot_box_cost
		if not await money.dm_check(self, ctx) and await money.permission(self, ctx.message.author.roles, 9):
			loot_box_cost = money
		else:
			await money.error_create(self, "You don't have enough permission to do that.", ctx)

def setup(client):
	client.add_cog(money(client))

