import discord
import asyncio
import random
import logging
import change_lang

global locs
global rules
global settings

logging.basicConfig(level=logging.INFO,
                    style = '{',
                    datefmt = "%d.%m.%Y %H:%M:%S",
                    format = "\n{asctime} [{levelname:<8}] {name}:\n{message}",
                    filename = "log.txt")

suggest = []
bot = discord.Client()

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='type !spyfall help'))
    print("Logged in as: " + (bot.user.name))
    print("ID: " + str(bot.user.id))
    print("READY!")
# setting up default lang
# rus/eng
locs, rules, settings = change_lang.set_lang('rus')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    elif message.content.startswith("!spyfall start"):
        global locs
        global rules
        global settings
        get_loc = random.choice(locs)
        get_spy = random.choice(message.author.voice.voice_channel.voice_members)
        await bot.send_message(message.channel, str(settings[6]))
        flag = 0
        player_list = message.author.voice.voice_channel.voice_members
        player_string = ''
        for player in player_list:
            if player == player_list[0]:
                player_string = player.mention
            else:
                player_string = player_string + ', ' + player.mention
            if player == get_spy:
                await bot.send_message(player, str(settings[1]))
            else:
                await bot.send_message(player, str(settings[2]) + ' ' + get_loc)
        await bot.send_message(message.channel, str(settings[7]) + player_string)

    elif message.content.startswith("!spyfall suggest"):
        await bot.send_message(message.channel, str(settings[3]))
        sure = await bot.wait_for_message(timeout=10.0, author=message.author)
        if sure.content == 'y':
            await bot.send_message(message.channel, str(settings[4]))
            new_loc = await bot.wait_for_message(timeout=10.0, author=message.author)
            f = open('suggest.txt', 'a')
            f.write(new_loc.content + '\n')
            print(new_loc.content)
            await bot.send_message(message.channel, str(settings[5]))
        else:
            await bot.send_message(message.channel, 'Okay :)')
        
    elif message.content.startswith("!spyfall setlang rus"):
        locs, rules, settings = change_lang.set_lang('rus')
        await bot.send_message(message.channel, "Успешно!")
        
    elif message.content.startswith("!spyfall setlang eng"):
        locs, rules, settings = change_lang.set_lang('eng')
        await bot.send_message(message.channel, "Success!")
        
    elif message.content.startswith("!spyfall rules"):
        await bot.send_message(message.channel, str(rules))
        
    elif message.content.startswith("!spyfall locs"):
        locs_string = ', '.join(locs)
        await bot.send_message(message.channel, locs_string)
        
    elif message.content.startswith("!spyfall help"):
        help_string = settings[0] + ''':
:flag_ru: !spyfall setlang rus
:flag_gb: !spyfall setlang eng
:closed_book: !spyfall rules
:camping: !spyfall locs
:writing_hand: !spyfall suggest
:game_die: !spyfall start
'''
        await bot.send_message(message.channel, help_string)
        
bot.run("place_your_token_here")
