from discord.ext import commands
import discord
import logging

class Poll(commands.Cog, name='Poll'):
    """Poll system allowing admin todo polls with 2-9 options"""
    def __init__(self, bot):
        self.bot = bot

    # create poll view that accepts question and options, asks user to select one option and then submits results
    class Poll(discord.ui.View):
        def __init__(self, question: str, options: str):
            super().__init__(timeout=None)
            self.question = question
            self.options = options
            self.message = None
            self.ctx = None
            self.votes: dict = {}
            self.results: dict = {}
            self.total_votes = 0
            self.results_message = None

            # create buttons for each option with callback
            for i, option in enumerate(self.options):
                self.add_item(self.GenericButton(label=option, style=discord.ButtonStyle.blurple, custom_id=str(i)))


        # create generic button with callback
        class GenericButton(discord.ui.Button):
            def __init__(self, label: str, style: discord.ButtonStyle, custom_id: str, emoji: str = None):
                super().__init__(label=label, style=style, custom_id=custom_id, emoji=emoji)

            async def callback(self, interaction: discord.Interaction):
                # try delete the message containing the button
                try:
                    # remove any previous votes from user
                    for custom_id in self.view.votes:
                        if interaction.user.id in self.view.votes[custom_id]:
                            self.view.votes[custom_id].remove(interaction.user.id)
                            self.view.total_votes -= 1
                    # add vote, custom id as key and add user id to list as value
                    if interaction.data['custom_id'] not in self.view.votes:
                        self.view.votes[interaction.data['custom_id']] = []
                    # add vote
                    self.view.votes[interaction.data['custom_id']].append(interaction.user.id)
                    self.view.total_votes += 1
                    # update results message
                    await self.view.results_message.edit(content=await self.view.get_results())
                    logging.info(f"{interaction.user} voted for '{self.label}' in poll '{self.view.question}'")
                    await interaction.response.defer()
                except Exception as e:
                    logging.error(e)

        async def get_results(self):
            """Get results of poll and return as string"""
            # create results dict
            for i, _ in enumerate(self.options):
                self.results[str(i)] = 0
            # add votes to results dict
            for custom_id in self.votes:
                self.results[custom_id] += len(self.votes[custom_id])
            # create string to return
            results = f"Results for poll '{self.question}'\n"
            for i, option in enumerate(self.options):
                # be careful of zero division error
                if self.total_votes == 0:
                    results += f"{option}: {self.results[str(i)]} votes (0%)\n"
                else:
                    results += f"{option}: {self.results[str(i)]} votes ({round(self.results[str(i)]/self.total_votes*100, 2)}%)\n"
            return results

        # start poll
        async def start(self):
            # create results dict
            for i, _ in enumerate(self.options):
                self.results[str(i)] = 0
            # send message
            self.message = await self.ctx.channel.send(self.question, view=self)
            # send results message
            self.results_message = await self.ctx.channel.send(await self.get_results())
            logging.info(f"{self.ctx.author} started a poll in '{self.ctx.channel}' channel")


    @commands.command(name='poll', help='Given options and question, starts a poll', hidden=True)
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, question: str, *options: str):
        """Given options and question starts a poll, must be administrator.

        Parameters
        ----------
        question : str
            Question to ask
        options : *str
            Options to choose from
        """
        # try delete the message containing the command
        try:
            await ctx.message.delete()
        except Exception as e:
            logging.error(e)
        # create poll and send
        poll = self.Poll(question, options)
        poll.ctx = ctx
        await poll.start()
        logging.info(f"{ctx.author} started a poll in '{ctx.channel}' channel")


async def setup(bot):
    await bot.add_cog(Poll(bot))