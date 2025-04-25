import hikari
import hikari.embeds
import lightbulb
import json
import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from mal import AnimeSearch

plugin = lightbulb.Plugin("next")

color = 9937663

def scrape(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    iframes = soup.find_all("iframe")

    for frame in iframes:
        src = frame.get('src')
        if src and "dailymotion" in src:
            iframe = src

    if "?pubtool=oembed" in iframe: return iframe.replace("?pubtool=oembed", "")
    if "geo.dailymotion.com" in iframe: 
        last = iframe.split("=")[1]
        last = last[-1]
        id = iframe.split("=")[1].replace(last, "")
        return f"https://www.dailymotion.com/embed/video/{id}"
    else: return soup.find("iframe")['src']

@plugin.command
@lightbulb.command("next", "next episode url.")
@lightbulb.implements(lightbulb.SlashCommand)
async def next(ctx):
    cluster = MongoClient("mongodb+srv://amgonzalez582:ukxQVd1pbdBnXIBG@yun.khkvxol.mongodb.net/?retryWrites=true&w=majority&appName=Yun")
    db = cluster['Discord']
    collection = db['Donghua']

    selected = collection.find_one({"_id": "selected"})['title']
    title = collection.find_one({"title": {"$regex": f".*{selected}.*", "$options": "i"}, "_id": {"$ne": "selected"}})['title'].split(" / ")[0]
    altTitle = collection.find_one({"title": {"$regex": f".*{selected}.*", "$options": "i"}, "_id": {"$ne": "selected"}})['title'].split(" / ")[1]
    episode = collection.find_one({"title": {"$regex": title or altTitle, "$options": "i"}, "_id": {"$ne": "selected"}})['episode']
    skipTime = collection.find_one({"title": {"$regex": title or altTitle, "$options": "i"}, "_id": {"$ne": "selected"}})['skipTime']

    name = title

    try: 
        url = collection.find_one({"title": {"$regex": title or altTitle, "$options": "i"}, "_id": {"$ne": "selected"}})['url'].format(episode)
    except: url = ""

    try: 
        args = collection.find_one({"title": {"$regex": title or altTitle, "$options": "i"}, "_id": {"$ne": "selected"}})['args'].capitalize()
    except: args = ""

    try:
        DMSettings = f"?autoplay=1&start={skipTime}&forcedQuality=1080"

        cover = AnimeSearch(title).results[0].image_url

        collection.update_one({"title": {"$regex": f".*{title}.*"}, "_id": {"$ne": "selected"}}, {"$inc": {"episode": 1}})
        episode = collection.find_one({"title": {"$regex": title or altTitle, "$options": "i"}, "_id": {"$ne": "selected"}})['episode']
        lessThan = lambda episode: '0' + str(episode) if episode < 10 else str(episode)
        response = requests.get(f"https://myanime.live/?s={name.replace(" ", "+")}+{args.replace(" ", "+")}+episode+{lessThan(episode)}").content
        soup = BeautifulSoup(response, "html.parser")
        date = soup.find('time', {"class": "entry-date"}).text.strip()
        lst = []
        for header in soup.find_all("h2", {"class": "entry-header-title"}):
            if name and str(episode) in header.a.text:
                lst.append(lst.append(header.a.get('href')))
                if len(lst) > 1: url = lst[0]
                else: url = header.a.get('href')

                #print("\n", date)
                #print(url)
        embed = (
            hikari.Embed(
                title=title,
                description=f"{args} Episode {episode}",
                color=color,
                url=scrape(url) + DMSettings
            )
            #.set_image(cover)
            .set_footer(date)
            .set_thumbnail(cover)
        )
        await ctx.respond(embed)

    except: 
            collection.update_one({"title": {"$regex": f".*{title}.*"}, "_id": {"$ne": "selected"}}, {"$inc": {"episode": -1}})
            await ctx.respond("You are on the most recent episode.", delete_after=2.5)
            
def load(bot):
    bot.add_plugin(plugin)