import hikari
import lightbulb
import random

plugin = lightbulb.Plugin("error")

color = 9937663

@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent):
    author = event.context.author.mention
    print(event)
    exception = event.exception.__cause__ or event.exception
    links = ["https://c.tenor.com/4q5OwnFZJdEAAAAC/adorable-pleading.gif",
             "https://i.pinimg.com/originals/4c/2e/b6/4c2eb6be4a6cecd2537df77e722dcfc4.gif",
             "https://c.tenor.com/kaRCm9ELxKgAAAAC/menhera-chan-chibi.gif",
             "https://c.tenor.com/w3-EnqpMxucAAAAC/cute-anime.gif",
             "https://64.media.tumblr.com/1522db257c8a8aadfd28391c265d19aa/60669299e894014d-8f/s540x810/b2d810c98a708002dd6a2fd1295474369f9911e6.gif",
             "https://c.tenor.com/H9ozhu1kZf0AAAAd/feeding-anime-cute.gif"]
    if isinstance(exception, lightbulb.NotOwner):
        gif = random.choice(links)
        embed = (
            hikari.Embed(
                description="Sorry {}, you do not\n have permissions to do that!".format(author),
                colour=color
            )
            .set_image(gif)
        )
        await event.context.respond(embed=embed)

    if isinstance(exception, lightbulb.MissingRequiredRole):
        gif = random.choice(links)
        embed = (
            hikari.Embed(
                description="Sorry {}, you do not\n have permissions to do that!".format(author),
                colour=color
            )
            .set_image(gif)
        )
        await event.context.respond(embed=embed)

    if isinstance(event.exception, lightbulb.CommandInvocationError):
        gif = random.choice(links)
        embed = (
            hikari.Embed(
                description="Sorry {}, something went wrong!".format(author),
                colour=color
            )
            .set_image(gif)
        )
        await event.context.respond(embed=embed)
        raise event.exception

def load(bot):
    bot.add_plugin(plugin)

