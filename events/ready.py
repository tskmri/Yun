import lightbulb
import hikari
import pymongo
from pymongo import MongoClient
import time

plugin = lightbulb.Plugin('ready')

@plugin.listener(hikari.StartedEvent)
async def on_ready(event):
    print("Ready to go!")

def load(bot):
    bot.add_plugin(plugin)
