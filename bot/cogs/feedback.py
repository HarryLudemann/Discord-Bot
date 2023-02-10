from discord.ext.commands import Cog, command
import discord
import logging
import discord

class FeedbackModal(discord.ui.Modal, title='Feedback'):
    """Modal containing the feedback questions"""
    name = discord.ui.TextInput(
        label='Name',
        placeholder='Your name here...',
        required=False,
    )
    feedback = discord.ui.TextInput(
        label='What do you think of this server?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=True,
        max_length=500,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

class FeedbackView(discord.ui.View):
    """View with button to send feedback modal"""
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(label='Send Feedback', style=discord.ButtonStyle.blurple)
    async def send_feedback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_modal(FeedbackModal())

class Feedback(Cog, name='Feedback'):
    """Feedback system allowing users to provide feedback"""
    def __init__(self, bot):
        self.bot = bot

    @command(name='feedback')
    async def feedback(self, ctx):
        try:
            await ctx.message.delete()
        except Exception as e:
            logging.error(e)
        await ctx.send('Please provide feedback', view=self.FeedbackView(ctx))


async def setup(bot):
    await bot.add_cog(Feedback(bot))