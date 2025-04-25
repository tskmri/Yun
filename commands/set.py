import hikari
import lightbulb
import json
import pymongo
from pymongo import MongoClient

plugin = lightbulb.Plugin("set")

@plugin.command
@lightbulb.option("title", "title of show")
#@lightbulb.option("mode", "search or url method.", required=False)
@lightbulb.command("set", "set the current show.")
@lightbulb.implements(lightbulb.SlashCommand)
async def set(ctx):
    cluster = MongoClient("mongodb+srv://amgonzalez582:ukxQVd1pbdBnXIBG@yun.khkvxol.mongodb.net/?retryWrites=true&w=majority&appName=Yun")
    db = cluster['Discord']
    collection = db['Donghua']

    selected = collection.find_one({"_id": "selected"})['title']
    title = collection.find_one({"title": {"$regex": f".*{selected}.*", "$options": "i"}, "_id": {"$ne": "selected"}})['title'].split(" / ")[0]
    altTitle = collection.find_one({"title": {"$regex": f".*{selected}.*", "$options": "i"}, "_id": {"$ne": "selected"}})['title'].split(" / ")[1]

    title = ctx.options.title
    collection.update_one({"_id": "selected"}, {"$set":{"title":title}})

    try:
        collection.update_one({"_id": "selected"}, {"$set": {"mode": "url"}})
        url = collection.find_one({"title": {"$regex": title or altTitle, "$options": "i"}, "_id": {"$ne": "selected"}})['url']
    except: collection.update_one({"_id": "selected"}, {"$set": {"mode": "search"}})

    await ctx.respond("Updated.", delete_after = 2.5)
 
def load(bot):
    bot.add_plugin(plugin)