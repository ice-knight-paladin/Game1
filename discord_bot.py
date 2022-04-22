import logging

import discord
from discord.ext import commands, tasks
import schedule
import wikipedia

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

config = {
    'token': '',
    'prefix': '!',
}

bot = commands.Bot(command_prefix=config['prefix'])


@bot.event
async def on_ready():
    print(f'{bot.user} подключен к Discord!')
    for guild in bot.guilds:
        print(
            f'{bot.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})'
        )


@bot.command()
async def kick(ctx, member: discord.Member, reason):
    await ctx.send("Изгоняем участника {0} по причине: {1}".format(member, reason))
    await member.ban(reason=f'{ctx.author} Выгнал {member}')


@bot.command()
async def tictoe(ctx):
    pol = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    try:

        await ctx.send("you play tic-tac-toe")

        with open("input.txt", "w") as f:
            f.write("1")

        @bot.event
        async def on_message(message):
            channel = message.channel
            try:
                if message.content == "end":
                    await channel.send("Pity")
                    return
                m = list(map(int, str(message.content).strip().split()))
                try:
                    if m[1] <= len(pol[0]) and m[0] <= len(pol) and pol[m[1] - 1][m[0] - 1] == 0:
                        with open("input.txt", "r") as f:
                            if f.readline() == "1":
                                pol[m[1] - 1][m[0] - 1] = "1"
                        with open("input.txt", "r") as f:
                            if f.readline() == "2":
                                pol[m[1] - 1][m[0] - 1] = "2"
                        for i in pol:
                            await channel.send(i)
                        await channel.send("Your turn")

                        with open("input.txt") as f:
                            if f.readline() == "2":
                                f.close()
                                d = True
                            else:
                                f.close()
                                d = False
                        if d:
                            with open("input.txt", "w") as f:
                                f.write("1")
                        else:
                            with open("input.txt", "w") as f:
                                f.write("2")
                        for i in range(3):
                            if pol[i][0] == pol[i][1] == pol[i][2] == "1" or pol[i][0] == pol[i][1] == pol[i][2] == "2":
                                await channel.send("Win")
                                return
                            if pol[0][i] == pol[1][i] == pol[2][i] == "1" or pol[0][i] == pol[1][i] == pol[2][i] == "2":
                                await channel.send("Win")
                                return
                        if pol[0][0] == pol[1][1] == pol[2][2] == "1" or pol[0][0] == pol[1][1] == pol[2][2] == "2":
                            await channel.send("Win")
                            return
                        if pol[2][0] == pol[1][1] == pol[0][2] == "1" or pol[2][0] == pol[1][1] == pol[0][2] == "2":
                            await channel.send("Win")
                            return
                except ValueError:
                    await channel.send("Клетка занята")
            except ValueError:
                pass

    except ValueError:
        pass


@bot.command()
async def example(ctx):
    import requests
    from bs4 import BeautifulSoup as b
    from random import choice
    URL = "https://www.matburo.ru/ex_tv.php?p1=tvklass"
    r = requests.get(URL)
    soup = b(r.text, 'html.parser')
    a = [i.text for i in soup.find_all('p')]
    a.remove(a[0])
    await ctx.send(choice(a))


@bot.command(command="help")
async def help_(ctx):
    await ctx.send("!tictoe - игра в крестики-нолики\n"
                   "!help - список команд\n"
                   "!kick - удаляет членов сервера\n"
                   "!wiki - отправляет {что это такое}/n"
                   "!translat - переводит слова на язык, который вы укажите")


@bot.command()
async def wiki(ctx, message):
    await ctx.send(wikipedia.summary(message))


@bot.command()
async def translat(ctx, message):
    g = message
    from translate import Translator

    @bot.event
    async def on_message(messag):
        channel = messag.channel
        translator = Translator(to_lang=g)
        translation = translator.translate(messag.content)
        if messag.author != bot.user:
            await channel.send(translation)
        if messag.author == bot.user:
            return


bot.run(config['token'])
schedule.run_pending()
