import discord
import os
import praw
import random
import requests
import googleapiclient.discovery
import typing
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.members = True

#reddit variables
reddit = praw.Reddit(client_id=os.getenv('REDDIT_APPID'),
                     client_secret=os.getenv('REDDIT_SECRET'),
                     user_agent=os.getenv('REDDIT_UAGENT'),
                    )

print(reddit.read_only)

#Google YT variables
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(
	api_service_name, api_version, developerKey=os.getenv('YT_KEY')
	)

# weather variables
api_key = os.getenv('WEATHER_KEY')
base_url = "http://api.openweathermap.org/data/2.5/weather?"

the420_quotes = [('I was about to write a good quote but then I got high and forgot it.'), ('I never joined high school, I joined school high.'), ('I wake up early in the morning and it feels so good. Smoking on some s**t that you wish you could.'), ('If somebody gives me a joint, I might smoke it, but I don’t go after it.'), ('When you smoke the herb, it reveals you to yourself.'), ('If I study high, take the test high, I\’ll get HIGH scores!'), ('You either love weed, or you’re wrong.'), ('I am always high because the universe is so low.'),
             ]

from discord.ext import commands
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(name='Your Mum', type=3))
    
@bot.event
async def on_message(message):
    # Bot not replying to themselves
    if message.author == bot.user or message.author.bot:
        return
    # send back up2 with a mention of the user who sent the inital message.
    if message.content.startswith('up2'):
      await message.channel.send(f"up2{message.author.mention}")

    await bot.process_commands(message)

# ping pong test command
@bot.command()
async def ping(ctx):
    bot.load_extension('cogs.tarkov')

# weather commands
@bot.command()
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}",
                              color=ctx.guild.me.top_role.color,
                              timestamp=ctx.message.created_at,)
            embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await channel.send(embed=embed)
    else:
        await channel.send("City not found.")



# Embed memes subreddit top50 posts
@bot.command()
async def meme(ctx):
      subreddit = reddit.subreddit("memes")
      allsubs = []
      top = subreddit.top(limit = 50)
      for submission in top: 
        allsubs.append(submission)      
      randomsub = random.choice(allsubs)
      name = randomsub.title 
      url = randomsub.url       
      em = discord.Embed(
        title = name, 
        color = discord.Color.blurple()
      )
      em.set_image(url = url)
      await ctx.send(embed = em)

# Embed footballmemes subreddit top50 posts
@bot.command(aliases=['soccermeme'])
async def footballmeme(ctx):
      subreddit = reddit.subreddit("footballmemes")
      allsubs = []
      top = subreddit.top(limit = 50)
      for submission in top: 
        allsubs.append(submission)      
      randomsub = random.choice(allsubs)
      name = randomsub.title 
      url = randomsub.url       
      em = discord.Embed(
        title = name, 
        color = discord.Color.blurple()
      )
      em.set_image(url = url)
      await ctx.send(embed = em)

@bot.command()
async def its420(ctx):
  response = random.choice(the420_quotes)
  await ctx.send(response)

#youtube search command

@bot.command()
async def search(ctx, *args):
	output = ''
	for word in args:
		output += str(word)
		output += ' '
	request = youtube.search().list(
		part="id,snippet",
		type='video',
		q=f"{output}",
		videoDuration='short',
		videoDefinition='high',
		maxResults=1,
		videoEmbeddable='true',
		fields="nextPageToken,items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
	)
	response = request.execute()
	chan = response['items'][0]['snippet']['channelId']
	title = response['items'][0]['snippet']['title']
	idd = response['items'][0]['id']['videoId']
	dsc = response['items'][0]['snippet']['description']
	embed = discord.Embed(url="https://www.youtube.com/watch?v={idd}")
#	embed.set_image(url=f"https://i.ytimg.com/vi/{idd}/mqdefault.jpg")
	request2 = youtube.channels().list(
        	part="snippet",
        	id=f"{chan}",
        )
	response2 = request2.execute()
	pfp = response2['items'][0]['snippet']['thumbnails']['default']['url']
	name = response2['items'][0]['snippet']['localized']['title']
	embed.set_author(
	name=name, url=f"https://www.youtube.com/channel/{chan}", icon_url=pfp)

	view = DropdownView(idd)
	await ctx.send(embed=embed, view=view)


class Dropdown(discord.ui.Select):
	def __init__(self, idd):
        	self.idd = idd
        	options = [
            		discord.SelectOption(
                		label='Link', description='Click for YouTube Link'),

        	]
        	super().__init__(placeholder='Pick Option', min_values=1, max_values=1, options=options)

async def callback(self, interaction: discord.Interaction):
	await interaction.response.send_message(f'Link: https://www.youtube.com/watch?v={self.idd}', ephemeral=True)


class DropdownView(discord.ui.View):
    	def __init__(self, idd):
        	super().__init__()
        	self.add_item(Dropdown(idd))


  
bot.run(os.getenv('TOKEN'))

