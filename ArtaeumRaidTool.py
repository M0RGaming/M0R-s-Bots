import discord
import asyncio
from discord.ext import commands
import re
import os

bot = commands.Bot(command_prefix='/')

token = os.environ["Token2"]


emotes = {
	'dps': ['<:magDPS:777982060320391219>','<:stamDPS:777982060622905375>'],
	'magDPS': ['<:magsorc:755916823261872199>','<:magplar:755916814898430042>','<:magdk:755916821227503636>','<:magden:755916806408896634>','<:magcro:755916820455882954>','<:magblade:755916820623654912>','<:magDPS:777982060320391219>'],
	'stamDPS': ['<:stamsorc:755916822406103050>','<:stamplar:755916818979356712>','<:stamdk:755916821210595488>','<:stamden:755916810527834202>','<:stamcro:755916821223178260>','<:stamblade:755916818987614218>','<:stamDPS:777982060622905375>'],
	'heal': ['<:healsorc:777960536343838760>','<:healplar:777960536159420487>','<:healdk:777960536511217664>','<:healden:777960536335450144>','<:healcro:777960536276467713>','<:healblade:777960536210014239>'],
	'tank': ['<:tanksorc:777960536766808165>','<:tankplar:777960536624201728>','<:tankdk:777960536632983592>','<:tankden:777960536603754546>','<:tankcro:777960536725520454>','<:tankblade:777960536620924949>'],
	'classes': ['<:sorc:776723019652792320>','<:templar:776723019652530186>','<:dk:776723019489083402>','<:warden:776723019422367744>','<:necro:776723019585552405>','<:nb:776723019283431456>']
}

MessageVersion = '2.0'



@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))






@bot.command(name='create')
async def create(ctx, Title, Date, Time, Description):

	messageTxt = "To sign up, click your role followed by your class below the message.\n<:stamDPS:777982060622905375> is Stamina DPS, <:magDPS:777982060320391219> is Magicka DPS, <:heal:777982060433375293> is Healer, and <:tank:777982060647415818> is Tank."
	embedData = {
		"title": f"{Title}",
		"description": f"{Description}",
		"fields": [
			{"name": "Date", "value": f"{Date}", "inline":True},
			{"name": "Time", "value": f"{Time}", "inline":True},
			{"name": "\u200B", "value": "――――――――――――――――――――", "inline":False},
			{"name": "DPS", "value": "\u200B", "inline":True},
			{"name": "Healers", "value": "\u200B", "inline":True},
			{"name": "Tanks", "value": "\u200B", "inline":True},
		],
		"footer": {
			"text": f"Message Type: Raid - V{MessageVersion}"
		},
		"color": 0x00FFFF
	}
	
	embed = discord.Embed().from_dict(embedData)
	if len(embed) > 6000:
		await ctx.send(f"<@{ctx.author.id}> The message you requested was too long. Give less options.")
	else:
		message = await ctx.send(content=messageTxt,embed=embed)
		await message.add_reaction('<:magDPS:777982060320391219>')
		await message.add_reaction('<:stamDPS:777982060622905375>')
		'''
		for x in emotes['magDPS']+emotes['stamDPS']:
			await message.add_reaction(x)
		'''
		await message.add_reaction('<:heal:777982060433375293>')
		await message.add_reaction('<:tank:777982060647415818>')
		for x in emotes['classes']:
			await message.add_reaction(x)
		await message.add_reaction('⛔')

@bot.command(name='edit')
async def edit(ctx, messageID, name, value):
	message = await ctx.channel.fetch_message(messageID)
	embed = message.embeds[0]
	await ctx.message.delete()
	if name == 'title':
		embed.title = value
	elif name == 'description':
		embed.description = value
	elif name == 'time':
		embed.set_field_at(1,name=embed.fields[1].name,value=value,inline=embed.fields[1].inline)
	elif name == 'date':
		embed.set_field_at(0,name=embed.fields[0].name,value=value,inline=embed.fields[0].inline)

	await message.edit(embed=embed)


@bot.event
async def on_command_error(ctx, exception):
	if str(ctx.command) == 'create':
		if not len(ctx.args) == 5:
			embedData = {
				"title": "The /create command failed due to not enough parameters.",
				"description": "Please re-send the command with the correct parameters.\n\n/create [Title] [Date] [Time] [Description]",
				"footer": {
					"text": "This message will self destruct after 30 seconds."
				},
				"color": 0xFF0000
			}
			embed = discord.Embed().from_dict(embedData)
			message = await ctx.send(embed=embed,delete_after=30)
			return
	else:
		embedData = {
			"title": f"The /{ctx.command} command failed.",
			"description": f"{exception}",
			"footer": {
				"text": "This message will self destruct after 30 seconds."
			},
			"color": 0xFF0000
		}
		embed = discord.Embed().from_dict(embedData)
		message = await ctx.send(embed=embed,delete_after=30)
		return
		#print(f"Error in command {ctx.command}, {exception}")
	raise exception

@bot.event
async def on_raw_reaction_add(payload):
	await update_numbers(payload)
'''	
@bot.event
async def on_raw_reaction_remove(payload):
	await update_numbers(payload)
'''

async def update_numbers(payload):
	#channel = bot.get_channel(payload.channel_id)
	#message = await channel.fetch_message(payload.message_id)
	message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)



	#print(payload.emoji)

	### TEST TO SEE IF WE SHOULD RETURN ###

	if (message.embeds == []) or (payload.user_id == bot.user.id):
		return
	if message.embeds[0].footer.text == f"Message Type: Raid - V{MessageVersion}":
		embed = message.embeds[0]
		#user = await bot.fetch_user(payload.user_id)
		user = discord.Object(payload.user_id)
		emote = str(payload.emoji)

		

		dps = getVals(embed,3)
		heal = getVals(embed,4)
		tank = getVals(embed,5)

		# TODO: CHANGE THIS WHEN CLASS SYSTEMS ARE ADDED
		if emote in emotes['dps']:
		#if (emote in emotes['stamDPS']) or (emote in emotes['magDPS']):
			# if they clicked DPS
			
			ind = find(str(user.id),dps)
			heal = findAndRemove(str(user.id), heal)
			tank = findAndRemove(str(user.id), tank)


			if ind == -1:
				dps.append([emote,str(user.id)])
			else:
				dps[ind][0] = emote


			dpsOut = parseVals(dps)
			healOut = parseVals(heal)
			tankOut = parseVals(tank)

			embed.set_field_at(3,name=embed.fields[3].name,value=dpsOut,inline=embed.fields[3].inline)
			embed.set_field_at(4,name=embed.fields[4].name,value=healOut,inline=embed.fields[4].inline)
			embed.set_field_at(5,name=embed.fields[5].name,value=tankOut,inline=embed.fields[5].inline)


		elif emote == '<:heal:777982060433375293>':
			# if they clicked Heal
			
			ind = find(str(user.id),heal)
			dps = findAndRemove(str(user.id), dps)
			tank = findAndRemove(str(user.id), tank)

			
			if ind == -1:
				heal.append([emote,str(user.id)])
			else:
				heal[ind][0] = emote


			dpsOut = parseVals(dps)
			healOut = parseVals(heal)
			tankOut = parseVals(tank)

			embed.set_field_at(3,name=embed.fields[3].name,value=dpsOut,inline=embed.fields[3].inline)
			embed.set_field_at(4,name=embed.fields[4].name,value=healOut,inline=embed.fields[4].inline)
			embed.set_field_at(5,name=embed.fields[5].name,value=tankOut,inline=embed.fields[5].inline)

		elif emote == '<:tank:777982060647415818>':
			# if they clicked Tank
			
			ind = find(str(user.id),tank)
			dps = findAndRemove(str(user.id), dps)
			heal = findAndRemove(str(user.id), heal)

			
			if ind == -1:
				tank.append([emote,str(user.id)])
			else:
				tank[ind][0] = emote


			dpsOut = parseVals(dps)
			healOut = parseVals(heal)
			tankOut = parseVals(tank)

			embed.set_field_at(3,name=embed.fields[3].name,value=dpsOut,inline=embed.fields[3].inline)
			embed.set_field_at(4,name=embed.fields[4].name,value=healOut,inline=embed.fields[4].inline)
			embed.set_field_at(5,name=embed.fields[5].name,value=tankOut,inline=embed.fields[5].inline)

		elif emote in emotes['classes']:
			# if they clicked any of the classes

			classind = emotes['classes'].index(emote)

			ind = find(str(user.id),dps)
			if ind == -1:
				ind = find(str(user.id),heal)
				if ind == -1:
					ind = find(str(user.id),tank)
					if ind == -1:
						# if none are found
						await message.remove_reaction(payload.emoji, user)
						return
					else:
						# If they are in Tanks
						tank[ind][0] = emotes['tank'][classind]

				else:
					# If they are in Heals
					heal[ind][0] = emotes['heal'][classind]


			else:
				# If they are in DPS
				if dps[ind][0] in emotes['magDPS']:
					dps[ind][0] = emotes['magDPS'][classind]
				elif dps[ind][0] in emotes['stamDPS']:
					dps[ind][0] = emotes['stamDPS'][classind]


			dpsOut = parseVals(dps)
			healOut = parseVals(heal)
			tankOut = parseVals(tank)

			embed.set_field_at(3,name=embed.fields[3].name,value=dpsOut,inline=embed.fields[3].inline)
			embed.set_field_at(4,name=embed.fields[4].name,value=healOut,inline=embed.fields[4].inline)
			embed.set_field_at(5,name=embed.fields[5].name,value=tankOut,inline=embed.fields[5].inline)






		elif str(payload.emoji) == '⛔':

			dps = findAndRemove(str(user.id), dps)
			heal = findAndRemove(str(user.id), heal)
			tank = findAndRemove(str(user.id), tank)

			dpsOut = parseVals(dps)
			healOut = parseVals(heal)
			tankOut = parseVals(tank)

			embed.set_field_at(3,name=embed.fields[3].name,value=dpsOut,inline=embed.fields[3].inline)
			embed.set_field_at(4,name=embed.fields[4].name,value=healOut,inline=embed.fields[4].inline)
			embed.set_field_at(5,name=embed.fields[5].name,value=tankOut,inline=embed.fields[5].inline)
		





		await message.edit(embed=embed) # after everything is updated, push the update to the message
		await message.remove_reaction(payload.emoji, user) 



def getVals(embed,field):
	newValue = '\u200b'
	currentVal = embed.fields[field].value.replace('\u200b','')
	cleanedUpVal = re.sub(r'<(.*?)> <@(.*?)>',r'<\1> \2',currentVal)
	valList = cleanedUpVal.split("\n")

	# if list is empty, return [], otherwise return the double split list.
	return [] if valList == [''] else [i.split(' ') for i in valList]

	#return 

def parseVals(vals):
	outlist = []
	for x in vals:
		outlist.append(f'{x[0]} <@{x[1]}>')
	if outlist == []:
		return '\u200b'
	else:
		return '\n'.join(outlist)


def findAndRemove(val, li):
	for x in li:
		if x[1] == val:
			li.remove(x)
			break
	return li

def find(val, li):
	ind = -1
	for x in li:
		if x[1] == val:
			ind = li.index(x)
			break
	return ind

#bot.run('')
bot.run(token)