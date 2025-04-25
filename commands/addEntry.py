import hikari
import lightbulb
import json
import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from AnilistPython import Anilist
anilist = Anilist()

plugin = lightbulb.Plugin("addEntry")

@plugin.command
@lightbulb.option("url", "url for show from myanime.live", required=False)
@lightbulb.option("args", "additional arguments for url, such as 'season 5'.", required=False)
@lightbulb.option("start", "when the episode starts.", type=int)
@lightbulb.option("episode", "the current episode.", type=int)
@lightbulb.option("title", "title of the show.")
@lightbulb.command("add", "add a new entry.")
@lightbulb.implements(lightbulb.SlashCommand)
async def current(ctx):
    cluster = MongoClient("mongodb+srv://amgonzalez582:ukxQVd1pbdBnXIBG@yun.khkvxol.mongodb.net/?retryWrites=true&w=majority&appName=Yun")
    db = cluster['Discord']
    collection = db['Donghua']

    title = ctx.options.title
    episode = ctx.options.episode
    start = ctx.options.start
    url = ctx.options.url
    args = ctx.options.args

    anime = anilist.get_anime(title)
    english = anime.get("name_english")
    native = anime.get("name_romaji")
    aniURL = f"https://anilist.co/anime/{id}"

    r = requests.get(aniURL).content
    soup = BeautifulSoup(r, "html.parser")

    #if english == None:
        #id = anilist.get_anime_id(title)
        #length = len(soup.find_all("div", {"class": "value"})) - 1 
        #title = soup.find_all("div", {"class": "value"})[length].text.strip()

    if title == native: title = f"{native} / {english}"
    else: title = f"{english} / {native}"

    titleExists = collection.find_one({"title": {"$regex": title, "$options": "i"}, "_id": {"$ne": "selected"}}) != None

    if url == None:
        post = {"title": title, "episode": episode, "skipTime": start}

        if args != None:
            post = {"title": title, "episode": episode, "skipTime": start, "args": args}

    
    else: post = {"title": title, "episode": episode, "skipTime": start, "url": url}

    if not titleExists: 
        collection.insert_one(post) 
        await ctx.respond("Added.", delete_after=2.5)

    else: await ctx.respond("Already exists.", delete_after=2.5)
 
def load(bot):
    bot.add_plugin(plugin)