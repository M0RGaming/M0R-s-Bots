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
	'heal': ['<:healsorc:777960536343838760>','<:healplar:777960536159420487>','<:healdk:777960536511217664>','<:healden:777960536335450144>','<:healcro:777960536276467713>','<:healblade:777960536210014239>','<:heal:777982060433375293>'],
	'tank': ['<:tanksorc:777960536766808165>','<:tankplar:777960536624201728>','<:tankdk:777960536632983592>','<:tankden:777960536603754546>','<:tankcro:777960536725520454>','<:tankblade:777960536620924949>','<:tank:777982060647415818>'],
	'classes': ['<:sorc:776723019652792320>','<:templar:776723019652530186>','<:dk:776723019489083402>','<:warden:776723019422367744>','<:necro:776723019585552405>','<:nb:776723019283431456>']
}

MessageVersion = '4.0'



@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))


@bot.command(name='create')
async def create(ctx, Title, Date, Time, Description='', limit='0,0,0'):


	limits = limit.split(',')
	errorDesc = 'The limits should be all positive integers.'
	try:
		if not len(limits) == 3:
			errorDesc = 'All of the limits are required.'
			raise NameError
		for x in range(len(limits)):
			limits[x] = int(limits[x])
	except:
		desc = f"{errorDesc}\nPlease re-send the command with the correct parameters.\nA [] parameters is required and a () parameters is optional.\n\n/create [Title] [Date] [Time] (Description) (DPS limits,Healer limits,Tank limits)"

		embedData = {
			"title": "The /create command failed due to invalid limits",
			"description": desc,
			"footer": {
				"text": "This message will self destruct after 30 seconds."
			},
			"color": 0xFF0000
		}
		embed = discord.Embed().from_dict(embedData)
		message = await ctx.send(embed=embed,delete_after=30)
		return

	if limits[0] == 0:
		limDPS = ''
	else:
		limDPS = f'/{limits[0]}'
	if limits[1] == 0:
		limHeal = ''
	else:
		limHeal = f'/{limits[1]}'
	if limits[2] == 0:
		limTank = ''
	else:
		limTank = f'/{limits[2]}'



	messageTxt = "To sign up, click your role followed by your class below the message.\n\n<:stamDPS:777982060622905375> is Stamina DPS, <:magDPS:777982060320391219> is Magicka DPS, <:heal:777982060433375293> is Healer, and <:tank:777982060647415818> is Tank.\n❓is for if you don't know if you can make it, and⌛is for if the group is filled.\n⛔is to be removed from the signups."
	embedData = {
		"title": f"{Title}",
		"description": f"{Description}",
		"fields": [
			{"name": "Date", "value": f"{Date}", "inline":True},
			{"name": "Time", "value": f"{Time}", "inline":True},
			{"name": "\u200B", "value": "\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_", "inline":False},
			{"name": f"DPS (0{limDPS})", "value": "\u200B", "inline":True},
			{"name": f"Healers (0{limHeal})", "value": "\u200B", "inline":True},
			{"name": f"Tanks (0{limTank})", "value": "\u200B", "inline":True},
			{"name": "\u200B", "value": "\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_", "inline":False},
			{"name": "Maybe (0)", "value": "\u200B", "inline":True},
			{"name": "Wait List (0)", "value": "\u200B", "inline":True},
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
		embed.set_footer(text=f"Message Type: Raid - V{MessageVersion}\nEvent ID: {message.id}")
		await message.edit(embed=embed)
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
		await message.add_reaction('❓')
		await message.add_reaction('⌛')
		await message.add_reaction('⛔')
		await ctx.message.delete()

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

@create.error
async def create_error(ctx, exception):
	args = ctx.args[1:]
	if len(args) == 2:
		error = 'The /create command failed due to having not enough parameters.'
		errorDesc = 'The Time parameter is required for this program to work.'
	elif len(args) == 1:
		error = 'The /create command failed due to having not enough parameters.'
		errorDesc = 'The Date and Time parameters are required for this program to work.'
	elif len(args) == 0:
		error = 'The /create command failed due to having not enough parameters.'
		errorDesc = 'No parameters were provided.'
	else:
		error = 'The /create command failed due to an unexpected error.'
		errorDesc = 'Please check your parameters and try again.'

	desc = f"{errorDesc}\nPlease re-send the command with the correct parameters.\nA [] parameters is required and a () parameters is optional.\n\n/create [Title] [Date] [Time] (Description) (DPS limits,Healer limits,Tank limits)"

	embedData = {
		"title": error,
		"description": desc,
		"footer": {
			"text": "This message will self destruct after 30 seconds."
		},
		"color": 0xFF0000
	}
	embed = discord.Embed().from_dict(embedData)
	message = await ctx.send(embed=embed,delete_after=30)




@bot.event
async def on_command_error(ctx, exception):
	if str(ctx.command) == 'create':
		return
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
	if payload.user_id == bot.user.id:
		return
	message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)



	#print(payload.emoji)

	### TEST TO SEE IF WE SHOULD RETURN ###

	if message.embeds == []:
		return
	if f"Message Type: Raid - V{MessageVersion}" in message.embeds[0].footer.text:
		embed = message.embeds[0]
		#user = await bot.fetch_user(payload.user_id)
		user = discord.Object(payload.user_id)
		emote = str(payload.emoji)

		

		dps = getVals(embed,3)
		heal = getVals(embed,4)
		tank = getVals(embed,5)
		maybe = getVals(embed,7)
		waitList = getVals(embed,8)

		limDPS = embed.fields[3].name
		if '/' in limDPS:
			limDPS = int(limDPS.split('/')[1].replace(')',''))
		else:
			limDPS = 0
		limHeal = embed.fields[4].name
		if '/' in limHeal:
			limHeal = int(limHeal.split('/')[1].replace(')',''))
		else:
			limHeal = 0
		limTank = embed.fields[5].name
		if '/' in limTank:
			limTank = int(limTank.split('/')[1].replace(')',''))
		else:
			limTank = 0



		# ROLE SYSTEMS
		if emote in emotes['dps']:
			heal = findAndRemove(str(user.id), heal)
			tank = findAndRemove(str(user.id), tank)
			maybe = findAndRemove(str(user.id), maybe)
			ind = find(str(user.id),dps)

			if (len(dps) >= limDPS) and (ind == -1) and (not limDPS == 0):
				ind = find(str(user.id),waitList)
				dps = findAndRemove(str(user.id), dps)
				if ind == -1:
					waitList.append([emote,str(user.id)])
				else:
					waitList[ind][0] = emote
			else:
				waitList = findAndRemove(str(user.id), waitList)
				if ind == -1:
					dps.append([emote,str(user.id)])
				else:
					dps[ind][0] = emote

		


		elif emote == '<:heal:777982060433375293>':
			# if they clicked Heal
			dps = findAndRemove(str(user.id), dps)
			tank = findAndRemove(str(user.id), tank)
			maybe = findAndRemove(str(user.id), maybe)
			ind = find(str(user.id),heal)
			if (len(heal) >= limHeal) and (ind == -1) and (not limHeal == 0):
				ind = find(str(user.id),waitList)
				heal = findAndRemove(str(user.id), heal)
				if ind == -1:
					waitList.append([emote,str(user.id)])
				else:
					waitList[ind][0] = emote
			else:
				waitList = findAndRemove(str(user.id), waitList)
				if ind == -1:
					heal.append([emote,str(user.id)])
				else:
					heal[ind][0] = emote
			
			


		elif emote == '<:tank:777982060647415818>':
			# if they clicked Tank
			
			dps = findAndRemove(str(user.id), dps)
			heal = findAndRemove(str(user.id), heal)
			maybe = findAndRemove(str(user.id), maybe)
			ind = find(str(user.id),tank)
			if (len(tank) >= limTank) and (ind == -1) and (not limTank == 0):
				ind = find(str(user.id),waitList)
				tank = findAndRemove(str(user.id), tank)
				if ind == -1:
					waitList.append([emote,str(user.id)])
				else:
					waitList[ind][0] = emote
			else:
				waitList = findAndRemove(str(user.id), waitList)
				if ind == -1:
					tank.append([emote,str(user.id)])
				else:
					tank[ind][0] = emote

		
		elif emote in emotes['classes']:
			# if they clicked any of the classes

			classind = emotes['classes'].index(emote)

			ind = find(str(user.id),dps)
			if ind == -1:
				ind = find(str(user.id),heal)
				if ind == -1:
					ind = find(str(user.id),tank)
					if ind == -1:
						ind = find(str(user.id),waitList)
						if ind == -1:
							# if none are found
							await message.remove_reaction(payload.emoji, user)
							return
						else:
							#If they are in the Wait List
							if waitList[ind][0] in emotes['magDPS']:
								waitList[ind][0] = emotes['magDPS'][classind]
							elif waitList[ind][0] in emotes['stamDPS']:
								waitList[ind][0] = emotes['stamDPS'][classind]
							elif waitList[ind][0] in emotes['heal']:
								waitList[ind][0] = emotes['heal'][classind]
							elif waitList[ind][0] in emotes['tank']:
								waitList[ind][0] = emotes['tank'][classind]
							else:
								waitList[ind][0] = emotes['classes'][classind]

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

		elif str(payload.emoji) == '❓':

			ind = find(str(user.id),maybe)

			dps = findAndRemove(str(user.id), dps)
			heal = findAndRemove(str(user.id), heal)
			tank = findAndRemove(str(user.id), tank)
			waitList = findAndRemove(str(user.id), waitList)

			if ind == -1:
				maybe.append([emote,str(user.id)])
			else:
				maybe[ind][0] = emote

		elif str(payload.emoji) == '⌛':

			ind = find(str(user.id),waitList)

			dps = findAndRemove(str(user.id), dps)
			heal = findAndRemove(str(user.id), heal)
			tank = findAndRemove(str(user.id), tank)
			maybe = findAndRemove(str(user.id), maybe)

			if ind == -1:
				waitList.append([emote,str(user.id)])
			else:
				waitList[ind][0] = emote

		elif str(payload.emoji) == '⛔':

			dps = findAndRemove(str(user.id), dps)
			heal = findAndRemove(str(user.id), heal)
			tank = findAndRemove(str(user.id), tank)
			maybe = findAndRemove(str(user.id), maybe)
			waitList = findAndRemove(str(user.id), waitList)

		else:
			await message.remove_reaction(payload.emoji, user)
			return


		dpsOut = parseVals(dps)
		healOut = parseVals(heal)
		tankOut = parseVals(tank)
		maybeOut = parseVals(maybe)
		waitListOut = parseVals(waitList)

		if limDPS == 0:
			limDPSOut = ''
		else:
			limDPSOut = f'/{limDPS}'
		if limHeal == 0:
			limHealOut = ''
		else:
			limHealOut = f'/{limHeal}'
		if limTank == 0:
			limTankOut = ''
		else:
			limTankOut = f'/{limTank}'

		embed.set_field_at(3,name=f"DPS ({len(dps)}{limDPSOut})",value=dpsOut,inline=embed.fields[3].inline)
		embed.set_field_at(4,name=f"Healers ({len(heal)}{limHealOut})",value=healOut,inline=embed.fields[4].inline)
		embed.set_field_at(5,name=f"Tanks ({len(tank)}{limTankOut})",value=tankOut,inline=embed.fields[5].inline)
		embed.set_field_at(7,name=f"Maybe ({len(maybe)})",value=maybeOut,inline=embed.fields[7].inline)
		embed.set_field_at(8,name=f"Wait List ({len(waitList)})",value=waitListOut,inline=embed.fields[8].inline)




		await message.edit(embed=embed) # after everything is updated, push the update to the message
		await message.remove_reaction(payload.emoji, user) 



def getVals(embed,field):
	newValue = '\u200b'
	currentVal = embed.fields[field].value.replace('\u200b','')
	#cleanedUpVal = re.sub(r'<(.*?)> <@(.*?)>',r'<\1> \2',currentVal)
	cleanedUpVal = re.sub(r'(❓|⌛|.*?) <@(.*?)>',r'\1 \2',currentVal)
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