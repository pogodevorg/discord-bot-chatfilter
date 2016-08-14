import asyncio
import discord
import logging
import re

from filter_bot.workers import BaseWorker
from filter_bot import logger


class ChannelManagement(BaseWorker):

    def initialize(self):
        pass

    def run(self):

        self.client.loop.create_task(self.filter())

    async def filter(self):

        await self.client.wait_until_ready()

        # get arrays channels id need to post
        discord_channels = []
        for server in self.client.servers:
            for channel in server.channels:
                if channel.name in self.config.get('channels', []):
                    discord_channels.append(
                        discord.Object(channel.id))

        while not self.client.is_closed:
            for channel in discord_channels:
                await self.client.send_message(channel, message)

            await asyncio.sleep(300)

    def need_to_delete(self, message):

        except_roles = self.config.get('except_roles', [])

        # Do nothing if bot is sending message
        if message.author == self.client.user:
            return False

        """
        Ignore if message from except roles
        """
        for role in message.author.roles:
            if role.name in except_roles:
                return False

        """
        Check if message contains role name
        """
        pattern = "^\!(?i)(uptime|status).*$"
        # Manage channel filter
        if message.channel.name in self.config.get('channels', []):
            if (re.match(pattern, message.content)):
                # Log & print out
                log_message = 'Message has been deleted: {} - Author: {}'.format(
                    message.content, message.author.name)
                logger.log(log_message)
                logging.warning(log_message)

                # Delete message if matches pattern
                return True

    def _is_blacklisted(self, message_content):
        """ Check if there is blacklisted word in message or not """

        blacklist = self.config.get('blacklist', [])

        # If blacklist is empty dont use black list
        if len(blacklist) == 0:
            return False

        for word in blacklist:
            if word in message_content:
                return True
