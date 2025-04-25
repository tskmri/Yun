import hikari
import lightbulb
import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from mal import AnimeSearch

plugin = lightbulb.Plugin("behind")

color = 9937663

@plugin.command
@lightbulb.command("behind", "how many episodes behind you are.")
@lightbulb.implements(lightbulb.SlashCommand)
async def behind(ctx):
    cluster = MongoClient("mongodb+srv://amgonzalez582:ukxQVd1pbdBnXIBG@yun.khkvxol.mongodb.net/?retryWrites=true&w=majority&appName=Yun")
    db = cluster['Discord']
    collection = db['Donghua']

    selected = collection.find_one({"_id": "selected"})['title']
    title = collection.find_one({"title": {"$regex": f".*{selected}.*", "$options": "i"}, "_id": {"$ne": "selected"}})['title'].split(" / ")[0]
    altTitle = collection.find_one({"title": {"$regex": f".*{selected}.*", "$options": "i"}, "_id": {"$ne": "selected"}})['title'].split(" / ")[1]
    episode = collection.find_one({"title": {"$regex": title or altTitle, "$options": "i"}, "_id": {"$ne": "selected"}})['episode']
    
    cover = AnimeSearch(title).results[0].image_url

    condition = True
    page = 0

    while condition:
        response = requests.get(f"https://myanime.live/page/{page}").text
        soup = BeautifulSoup(response, "html.parser")
        page += 1
        headers = soup.find_all("h2", {"class": "entry-header-title"})
        for header in headers:
            if "100.000 Years of Refining Qi".lower() in header.text.lower():
                most_recent_episode = int(header.text.split("episode ")[1].split(" ")[0])
                if most_recent_episode != episode:
                    difference = abs(episode - most_recent_episode)
                    embed = (
                        hikari.Embed(
                            title=f"{title} \n({altTitle})",
                            description=f"You are {difference} episodes behind.",
                            color=color
                        )
                        .set_thumbnail(cover)
                    )
                    await ctx.respond(embed)
                else: await ctx.respond("You're on the most recent episode.", delete_after=2.5)
                condition = False

 
def load(bot):
    bot.add_plugin(plugin)