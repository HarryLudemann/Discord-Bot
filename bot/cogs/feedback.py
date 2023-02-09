from discord.ext.commands import Cog, command
import discord
import logging
import discord
import traceback

class FeedbackModal(discord.ui.Modal, title='Feedback'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    name = discord.ui.TextInput(
        label='Name',
        placeholder='Your name here...',
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    feedback = discord.ui.TextInput(
        label='What do you think of this server?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)



class Feedback(Cog, name='Feedback'):
    def __init__(self, bot):
        self.bot = bot

    class FeedbackView(discord.ui.View):
        # has button to send Feedback modal
        def __init__(self, ctx):
            super().__init__(timeout=None)
            self.ctx = ctx

        @discord.ui.button(label='Send Feedback', style=discord.ButtonStyle.blurple)
        async def send_feedback(self, button: discord.ui.Button, interaction: discord.Interaction):
            await button.response.send_modal(FeedbackModal())

        

    @command(name='feedback')
    async def feedback(self, ctx):
        try:
            await ctx.message.delete()
        except Exception as e:
            logging.error(e)
        await ctx.send('Please provide feedback', view=self.FeedbackView(ctx))


async def setup(bot):
    await bot.add_cog(Feedback(bot))