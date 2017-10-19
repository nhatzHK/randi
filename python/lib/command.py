import client_helpers as CLIENT
import discord

class CommandManager:
    def __init__ (
            self, 
            client, 
            refs, 
            index, 
            black_list, 
            dict_com, 
            config, 
            help_embed):
        self.client = client
        self.refs = refs
        self.index = index
        self.black_list = black_list
        self._dict_com = dict_com
        self.com = list (self._dict_com.keys ())
        self.config = config
        self.help_embed = help_embed
        self.report_feedback = discord.Embed (
                description = "_Your report has been transmitted. \
                        \nThank you for contributing in making me better_",
                colour = (0x00ff00))
        self.not_found_message = discord.Embed (
                description = "_I found nothing. I'm so sawry and sad :(_. \
                        \nReply with **`random`** for a surprise\n",
                colour = (0x000000))
        
    async def run (self, message, command, args):
        try:
            f_name = self._dict_com[command]
            f = CommandManager.__getattribute__ (self, f_name)
            await f (self, message, command, args)
        except AttributeError as ne:
            raise NameError ("Attribute {f_name} not found.") from ne
        except KeyError as ke:
            raise KeyError (f"No match found for {command}.") from ke
    
    @staticmethod
    async def random (coma, message, command, args):
        embed_comic = await CLIENT.random_embed (coma.refs)
        await coma.client.send_message (message.channel, embed = embed_comic)

    @staticmethod
    async def latest (coma, message, command, args):
        online_latest = await CLIENT.get_online_xkcd ()

        if online_latest['status'] is 0:
            embed_comic = await CLIENT.create_embed (online_latest)
        else:
            local_latest = xkc_refs[str (max (list (xkcd_refs.keys ())))]
            embed_comic = await CLIENT.create_embed (local_latest)

        await coma.client.send_message (message.channel, embed = embed_comic)

    @staticmethod
    async def report (coma, message, command, args):
        chan = coma.client.get_channel (coma.config['report_channel'])
        embed_report = await CLIENT.report_embed (
                message,
                {
                    'type'  : 'User',
                    'color' : (0xff0000),
                    'client': coma.client
                })
        await coma.client.send_message (chan, embed = embed_report)
        await coma.client.send_message (
                message.channel, 
                embed = coma.report_feedback)

    @staticmethod
    async def help (coma, message, command, args):
        await coma.client.send_message (
                message.channel, 
                embed = coma.help_embed)

    @staticmethod
    async def search (coma, message, command, args):
        tmp = await coma.client.send_message (message.channel, 'Searching...')

        if len (args) == 0:
            await coma.client.edit_message (tmp, ' ')
            await CommandManager.random (coma, message, command, args)
        else:
            result = await CLIENT.search (
                    ' '.join (args),
                    coma.index,
                    coma.refs,
                    coma.black_list)
            if result['status'] == 0:
                comic_embed = await CLIENT.create_embed (result['comic'])
                await coma.client.edit_message (tmp, ' ', embed = comic_embed)
            else:
                await coma.client.edit_message (
                        tmp, 
                        ' ', 
                        embed = coma.not_found_message)
                
                msg = await coma.client.wait_for_message (
                        author = message.author,
                        content = "random",
                        timeout = 20)

                if msg:
                    await coma.client.edit_message (tmp, ' ')
                    await CommandManager.random (coma, message, command, args)
                else:
                    await coma.client.edit_message (tmp, "**Timeout**")
