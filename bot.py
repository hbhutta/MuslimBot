import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import requests
import random
import json
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


intents = discord.Intents().default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
CHANNEL_ID = 1187541417099280456

async def fajr():
    c = bot.get_channel(CHANNEL_ID)
    await c.send(f"Time for Fajr!")
    # with open('../assets/mosque.jpg') as f:
    #     picture = discord.File(f)
    #     await c.send(file=picture)

async def dhuhr():
    c = bot.get_channel(CHANNEL_ID)
    await c.send(f"Time for Dhuhr!")

async def asr():
    c = bot.get_channel(CHANNEL_ID)
    await c.send(f"Time for Asr!")

async def maghrib():
    c = bot.get_channel(CHANNEL_ID)
    await c.send(f"Time for Maghrib")
    
async def isha():
    c = bot.get_channel(CHANNEL_ID)
    await c.send(f"Time for Isha")

'''
Start waiting to get next day's timings
'''
@bot.event
async def on_ready():
    print(f'Connected client: {bot.user}')
    get_timings.start()
    print('Updated timings!')

    with open('prayers.json', 'r') as f:
        todays_timings = json.load(f)

    reminders = {
        fajr: todays_timings['Fajr'], 
        dhuhr: todays_timings['Dhuhr'], 
        asr: todays_timings['Asr'], 
        maghrib: todays_timings['Maghrib'],  
        isha: todays_timings['Isha'], 
    }

    scheduler = AsyncIOScheduler()

    for reminder in reminders:
        hour = reminders[reminder][:2]
        minute = reminders[reminder][3:]
        # print(hour, minute)
        scheduler.add_job(reminder, CronTrigger(hour=int(hour), minute=int(minute))) 

    scheduler.start()

@bot.command(name='info')
async def info(ctx):
    help_info = '''
    **Commands**:\n- `!hadith hadith_source`: Sends a random hadith from the given hadith source
    \t- `hadith_source` is one of: 'bukhari': (1, 7563), 'muslim': (1,3032), 'abudawud': (1,3998), 'ibnmajah': (1,4342), 'tirmidhi': (1,3956)
    '''
    await ctx.send(help_info)

'''
Get a random hadith from Bukhari
'''
@bot.command(name='hadith')
async def hadith(ctx, hadith_source):
    try: 
        sources = {'bukhari': [1, 7563], 'muslim': [1,3032], 'abudawud': [1,3998], 'ibnmajah': [1,4342], 'tirmidhi': [1,3956]}
        sources_keys = list(sources.keys())
        print(sources_keys)
        print(sources_keys[1])
        rand_source = sources_keys[random.randrange(0,4)]
        print(rand_source)
        # print(sources[sources[rand_source]])
        rand_hadith = random.randrange(sources[rand_source][0], sources[rand_source][1])
        print(rand_hadith)
        request = requests.get(f'https://random-hadith-generator.vercel.app/{hadith_source}/{rand_hadith}')
        if (request.status_code == 200):
            json = request.json()
            topic = json['data']['bookName']
            chapter = json['data']['chapterName']
            hadith = json['data']['hadith_english']
            narrated_by = json['data']['header']
            ref = json['data']['refno']
            formatted_hadith=f'Title: __**{chapter[9:]}**__\nTopic:**{topic}**__{narrated_by}__\n*{hadith}*\n[{ref}]'
            await ctx.send(formatted_hadith)
    except AssertionError as a:
        print("Given hadith_source is invalid. Please try again.")


'''
Get the specific verse from the specified chapter in the Quran
'''
@bot.command(name='surah')
async def surah(ctx, chapter: int, verse_start: int, verse_end: int):
    formatted_verse = ""
    for i in range(verse_start, verse_end+1):
        ayaAPI = requests.get(f'https://quranenc.com/api/v1/translation/aya/english_saheeh/{chapter}/{str(i)}')
        json = ayaAPI.json()
        arabic = json["result"]["arabic_text"]
        english = json["result"]["translation"]
        formatted_verse += f"# {arabic}\n *{english}*\n"
    formatted_verse += f"### Qur'an {chapter}:{verse_start}-{verse_end}"
    try:
        assert len(formatted_verse) < 2000
    except AssertionError as e:
        await ctx.send(f"The Qur'an excerpt length of {len(formatted_verse)} exceeds 2000 characters. Please try a smaller range.")


    

'''
Get updated prayer times every 24 hours
'''
@tasks.loop(hours=24)
async def get_timings() -> dict:
    request = requests.get(f"http://api.aladhan.com/v1/calendarByCity/{datetime.now().year}/{datetime.now().month}?city=Vancouver&country=Canada&method=2")
    if request.status_code != 200:
        return None
    timings = request.json()["data"][0]["timings"]
    prayers = {}
    for prayer in timings.keys():
        if prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
            prayers[prayer] = timings[prayer][:5]
            print(prayers[prayer])
    print("Prayers: ", prayers)
    with open('prayers.json', 'w') as f:
        json.dump(prayers, f)
    print("Updated prayer times!")

    await bot.get_channel(CHANNEL_ID).send(f'Prayer times: {prayers}. Check at {datetime.now()}')

with open('prayers.json', 'r') as f:
    todays_timings = json.load(f)
    

bot.run(os.getenv('TOKEN')) 