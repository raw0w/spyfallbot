import json
import random

import discord


class SpyfallBot(discord.Client):
    data: dict
    with open('lang.json', encoding="utf8") as json_file:
        data = json.load(json_file)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = 'rus'

    async def on_ready(self):
        game = discord.Game("type !spyfall help")
        await self.change_presence(status=discord.Status.idle, activity=game)

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.content.startswith("!spyfall start"):
            get_loc = random.choice(SpyfallBot.data[self.lang]['locs'])
            get_spy = random.choice(message.author.voice.channel.members)
            player_list = message.author.voice.channel.members
            player_string = ''
            for player in player_list:
                if player == player_list[0]:
                    player_string = player.mention
                else:
                    player_string += ', ' + player.mention
                if player == get_spy:
                    await player.send(SpyfallBot.data[self.lang]['settings']['spy'])
                else:
                    await player.send(SpyfallBot.data[self.lang]['settings']['loc'] + ' ' + get_loc)
            await message.channel.send(SpyfallBot.data[self.lang]['settings']['start'])
            await message.channel.send(SpyfallBot.data[self.lang]['settings']['players'] + player_string)


        elif message.content.startswith("!spyfall setlang rus"):
            self.lang = 'rus'
            await message.channel.send("Успешно!")

        elif message.content.startswith("!spyfall setlang eng"):
            self.lang = 'eng'
            await message.channel.send("Success!")

        elif message.content.startswith("!spyfall rules"):
            await message.channel.send(SpyfallBot.data[self.lang]['rules'])

        elif message.content.startswith("!spyfall locs"):
            locs_string = ', '.join(SpyfallBot.data[self.lang]['locs'])
            await message.channel.send(locs_string)

        elif message.content.startswith("!spyfall help"):
            help_string = SpyfallBot.data[self.lang]['settings']['cmd_list'] + ''':
    :flag_ru: !spyfall setlang rus
    :flag_gb: !spyfall setlang eng
    :closed_book: !spyfall rules
    :camping: !spyfall locs
    :game_die: !spyfall start
    '''
            await message.channel.send(help_string)


if __name__ == '__main__':
    bot = SpyfallBot()
    bot.run("Mzg5OTQzNjU5Mzc5OTQ5NTY4.Xcs5mA.riEajhqQsowf7C2_JUDgdP8LfIE")
