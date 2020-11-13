import discord
import asyncio
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='/')
letters = ["🇦","🇧","🇨","🇩","🇪","🇫","🇬","🇭","🇮","🇯","🇰","🇱","🇲","🇳","🇴","🇵","🇶","🇷","🇸","🇹","🇺","🇻","🇼","🇽","🇾","🇿"]

token = os.environ["Token"]


@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))






@bot.command(name='vote')
async def vote(ctx, question, *options):

	letters = ["🇦","🇧","🇨","🇩","🇪","🇫","🇬","🇭","🇮","🇯","🇰","🇱","🇲","🇳","🇴","🇵","🇶","🇷","🇸","🇹","🇺","🇻","🇼","🇽","🇾","🇿"]
	messageTxt = "React with the letters below to vote."
	embedData = {
		"title": question,
		"fields": [],
		"footer": {
			"text": "Message Type: Vote - V1.0"
		}
	}
	for optionInd in range(len(options)):
		embedData["fields"].append({
			"name": f"Option {letters[optionInd]}: {options[optionInd]}",
			"value":"`<                    >` 0% - 0 votes"
			})
	embed = discord.Embed().from_dict(embedData)
	if len(embedData) > 6000:
		await ctx.send(f"<@{ctx.author.id}> The message you requested was too long. Give less options.")
	else:
		message = await ctx.send(content=messageTxt,embed=embed)
		for optionInd in range(len(options)):
			await message.add_reaction(letters[optionInd])



@bot.event
async def on_raw_reaction_add(payload):
	await update_numbers(payload)
	
@bot.event
async def on_raw_reaction_remove(payload):
	await update_numbers(payload)
	

async def update_numbers(payload):
	channel = await bot.fetch_channel(payload.channel_id)
	message = await channel.fetch_message(payload.message_id)

	### TEST TO SEE IF WE SHOULD RETURN ###

	if (message.embeds == []) or (payload.user_id == bot.user.id):
		return
	if message.embeds[0].footer.text == "Message Type: Vote - V1.0":
		
		try:
			option = letters.index(str(payload.emoji))
			if option > len(message.embeds[0].fields)-1:
				return
		except ValueError:
			return


		### END TESTING ###



		embed = message.embeds[0]

		# Count votes and totals
		votes = []
		total = 0

		for x in message.reactions[:len(embed.fields)]:
			votes.append(x.count-1)
			total += x.count-1



		for optionFinal in range(len(embed.fields)): # For every field, update numbers
			field = embed.fields[optionFinal]
			if total == 0:
				fraction = 0
			else:
				fraction = (votes[optionFinal]/total)
			numhash = int(fraction*20)
			percentbar = ""
			for x in range(numhash):
				percentbar += "#"
			for x in range(20-numhash):
				percentbar += " "
			embed.set_field_at(optionFinal,name=field.name,value=f"`<{percentbar}>` {round(fraction*100,2)}% - {votes[optionFinal]} votes",inline=False)
		
		await message.edit(embed=embed) # after everything is updated, push the update to the message 






bot.run()