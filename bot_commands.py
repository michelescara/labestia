import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from datetime import date
from datetime import datetime
from discord import app_commands



class BotCommands(commands.Cog):

    def __init__(self, bot):
        self.bot=bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name = "lockall", description = "Blocca tutti i canali portando la slowmode a 10 minuti.")
    async def lockall(self, ctx):
        guild=ctx.guild
        for channel in guild.text_channels:
            await channel.edit(slowmode_delay=600)
        if (guild.system_channel):
            await guild.system_channel.send("**QUESTA E' UN'EMERGENZA!**\n\n_Tutti i canali sono stati bloccati per 10 minuti, attendete l'intervento di un amministratore._")
        print(ctx.response)
        await self.bot.say(content="🔒Canali bloccati!")

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name = "unlockall", description = "Sblocca tutti i canali riportando la slowmode a 10 secondi.")
    async def unlockall(self, ctx):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                await channel.edit(slowmode_delay=10)
        await ctx.response.send_message("🔓Canali sbloccati!")

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name='clear', description= "Elimina il numero di messaggi indicato.")
    async def clear(self, ctx, num_messages: int):
        deleted = await ctx.channel.purge(limit=num_messages+1)
        await ctx.response.send_message(f"Cancellati {len(deleted)} messaggi.", delete_after=5)

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name='dm', description= "Invia un messaggio in privato all'utente indicato.")
    async def dm(self, ctx, member: discord.Member, message):      
        await member.send(message)

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
    