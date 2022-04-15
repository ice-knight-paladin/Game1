import discord
from discord.ext import commands, tasks
import schedule
import time

config = {
    'token': '',
    'prefix': '!',
}

bot = commands.Bot(command_prefix=config['prefix'])


@bot.command()
async def kick(ctx, member: discord.Member, reason):
    await ctx.send("Изгоняем участника {0} по причине: {1}".format(member, reason))
    await member.ban(reason=f'{ctx.author} Выгнал {member}')


@bot.command()
async def set_timer(ctx, a):
    await ctx.send(f"Через {a} минут")

    @tasks.loop(minutes=int(a))
    async def yourname():
        await ctx.send("TIME")
        await bot.wait_until_ready()
        yourname.stop()

    @yourname.before_loop
    async def yourname2():
        await bot.wait_until_ready()

    yourname.start()


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
                    if m[1] <= len(pol[0]) and m[0] <= len(pol) and pol[m[1]-1][m[0]-1] == 0:
                        with open("input.txt", "r") as f:
                            if f.readline() == "1":
                                pol[m[1]-1][m[0]-1] = "1"
                        with open("input.txt", "r") as f:
                            if f.readline() == "2":
                                pol[m[1]-1][m[0]-1] = "2"
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
                    pass
            except ValueError:
                pass

    except ValueError:
        await ctx.send("!tictoe {number} {number} {number}")


bot.run(config['token'])
schedule.run_pending()
