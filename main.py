import lightbulb
import hikari
import os
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.environ.get("TOKEN")

client = lightbulb.BotApp(
    token=TOKEN,
    default_enabled_guilds=[1244099409185214615]
)

client.load_extensions_from("./commands")

client.load_extensions_from("./events")

client.sync_application_commands()

client.run(
    status=hikari.Status.IDLE,
    activity=hikari.Activity(
        name="with clouds",
        type=hikari.ActivityType.PLAYING,
    )
)
