#
# Python chat filter bot for discord
# Author: enjoy2000 | enjoy3013@gmail.com
# Modified By: fkndean | FilterBot
#
import discord
import json
import sys

from filter_bot import FilterBot, logger

client = discord.Client()

if __name__ == '__main__':

    @client.event
    async def on_ready():
        """ Connected to bot """

        logger.log('Logged in as')
        logger.log(client.user.name)
        logger.log(client.user.id)
        logger.log('------')

    config = {}
    with open('config.json') as output:
        # Load json to config object
        config = json.load(output)

    bot = FilterBot(client, config)
    api_key = config.get('api_key', 'NA')

    if api_key == 'NA':
        raise Exception('Please specify your api key!')

    @client.event
    async def on_message(message):
        if bot.on_message(message):
            await client.delete_message(message)
    bot.run_worker('ChannelManagement')


    client.run(api_key)
