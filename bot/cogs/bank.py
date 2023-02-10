from discord.ext.commands import Cog, command, has_permissions, MemberConverter
import logging
if __name__ != '__main__':
    from bot.util.database import BankDatabase

class Bank(Cog, name='Bank'):
    """User bank accounts"""
    def __init__(self, bot):
        self.bot = bot
        self.__database = BankDatabase()

    @Cog.listener()
    async def on_member_join(self, member):
        if not self.__database.user_exists(str(member.id)):
            self.__database.create_user(str(member.id))
            logging.info(f'Created bank account for {member}')

    @command(name='balance', aliases = ["bal"], help='Check your balance')
    async def bal(self, ctx, member: MemberConverter = None):
        """Check your balance.

        Parameters
        ----------
        ctx : commands.Context
            Context of the command
        member : commands.MemberConverter
            Optionally member to check balance of
        """
        if member is None:
            member = ctx.author
        balance = self.__database.get_user_balance(str(member.id))
        if balance is None:
            await ctx.send('You are not registered')
            return
        await ctx.send(f'{member} has {balance} coins')

    @command(name='pay', help='Pay another user')
    async def pay(self, ctx, member: MemberConverter, amount: int):
        """Pay another user.

        Parameters
        ----------
        ctx : commands.Context
            Context of the command
        member : commands.MemberConverter
            Member to pay
        amount : int
            Amount to pay
        """
        if amount < 0:
            await ctx.send('You cannot pay a negative amount')
            return
        if self.__database.get_user_balance(str(ctx.author.id)) < amount:
            await ctx.send('You do not have enough coins')
            return
        self.__database.pay_user(str(ctx.author.id), str(member.id), amount)
        await ctx.send(f'You paid {member} {amount} coins')

    @command(name='register', aliases = ["reg"], hidden=True)
    async def register(self, ctx):
        """Manually create an account.

        Parameters
        ----------
        ctx : commands.Context
            Context of the command
        """
        if self.__database.create_user(str(ctx.author.id)):
            await ctx.send(f'Account created for {ctx.author}')
        else:
            await ctx.send(f'Account already exists for {ctx.author}')
    
    @command(name='setbal', hidden=True)
    @has_permissions(administrator=True)
    async def setbal(self, ctx, member: MemberConverter, amount: int):
        """Set another user's balance, must have administrator permission.

        Parameters
        ----------
        ctx : commands.Context
            Context of the command
        member : commands.MemberConverter
            Member to set balance of
        amount : int
            Amount to set balance to
        """
        if amount < 0:
            await ctx.send('You cannot set a negative balance')
            return
        self.__database.set_user_balance(str(member.id), amount)
        await ctx.send(f'Set {member}\'s balance to {amount} coins')


async def setup(bot):
    await bot.add_cog(Bank(bot))