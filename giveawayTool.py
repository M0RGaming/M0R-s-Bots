import discord
import asyncio
from discord.ext import commands
import os
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
import random

bot = commands.Bot(command_prefix='/')
slash = SlashCommand(bot) 
token = os.environ["Token3"]

@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))


@slash.slash(name="giveaway")
async def echo(ctx,channelID,msgID,emote): # Normal usage.
	try:
		message = await bot.get_channel(int(channelID)).fetch_message(int(msgID))
		for x in message.reactions:
			if str(x) == emote:
				users = await x.users().flatten()
				winner = random.choice(users)
				await ctx.send(4,f'🎉Congratz!🎉\n\n<@{winner.id}> has won the giveaway!')
				return
		await ctx.send(3,"The parameters provided were incorrect.",hidden=True)
	except:
		await ctx.send(3,"The parameters provided were incorrect.",hidden=True)

'''
@bot.command(name='test')
async def test(ctx, channelID, msgID, emote):
	message = await bot.get_channel(int(channelID)).fetch_message(int(msgID))
	for x in message.reactions:
		if str(x) == emote:
			users = await x.users().flatten()
			winner = random.choice(users)
			await ctx.send(f'<@{winner.id}> has won the giveaway!')
			return
	
'''


bot.run(token)