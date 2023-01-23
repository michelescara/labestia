import datetime
import discord
from discord.ext import commands
from discord import app_commands
import captcha_generation

class ServerLogger(commands.Cog):

    def __init__(self, bot):

        self.log_channel = None

        for guild in bot.guilds:
            self.welcome_channel = discord.utils.get(guild.channels, name='⌈👋🏻⌋-𝘽𝙚𝙣𝙫𝙚𝙣𝙪𝙩𝙤')
            self.goodbye_channel = discord.utils.get(guild.channels, name='⌈🚪⌋-𝘼𝙙𝙙𝙞𝙤')
            self.log_channel=discord.utils.get(guild.channels, name='⌈📂⌋-𝗟𝗼𝗴')
           
        self.join_log_channel=self.log_channel
        self.leave_log_channel=self.log_channel
        self.edit_message_log_channel=self.log_channel
        self.delete_message_log_channel=self.log_channel
        self.ban_log_channel=self.log_channel
        self.unban_log_channel=self.log_channel
        self.voice_log_channel=self.log_channel

    @commands.Cog.listener()
    async def on_message(self, message):
        if "bestia" in message.content.lower():
           await message.add_reaction("🦍")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        dateOfCreation=member.created_at
        dateOfCreation=str(dateOfCreation.day)+"/"+str(dateOfCreation.month)+"/"+str(dateOfCreation.year)
        embed=discord.Embed(title="**"+member.name+"**#"+member.discriminator, description=member.mention+" è entrato nel server!", color=0x36ceff)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="username", value=member.name, inline=True)
        embed.add_field(name="id", value=member.id, inline=True)
        embed.add_field(name="data creazione", value=dateOfCreation, inline=True)
        if self.join_log_channel is not None:
            await self.join_log_channel.send(embed=embed)
        if self.welcome_channel is not None:
            await self.welcome_channel.send(f"Ciao {member.mention}, benvenuto in {member.guild.name}!")
        
        difference = datetime.datetime.now().date() - member.created_at.date()
        # se la differenza è inferiore a 14 giorni o l'utente non ha un avatar
        if difference.days < 14 or member.avatar is None:
            # assegna il ruolo "Sospetto" all'utente
            role = discord.utils.get(member.guild.roles, name="Sospetto®")
            await member.add_roles(role)
            await member.send("**ATTENZIONE!** Il tuo account risulta sospetto 🧐. Attendi l'intervento di un Capo®.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed=discord.Embed(title="**"+member.name+"**#"+member.discriminator, description=member.mention+" ha lasciato il server!", color=0xff0000)
        embed.set_thumbnail(url=member.avatar)
        if self.leave_log_channel is not None:
            await self.leave_log_channel.send(embed=embed)
        if self.goodbye_channel is not None:
            await self.goodbye_channel.send(f"{member.mention} ha lasciato il server, RIP 😢")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if self.delete_message_log_channel is not None:
            author=message.author
            embed=discord.Embed(title=author.name+"#"+author.discriminator, description="❌ Messaggio eliminato", color=0xff0000)
            embed.add_field(name="messaggio", value="```"+message.content+"```", inline=False)
            await self.delete_message_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.edit_message_log_channel is not None:
            author=before.author
            beforeMessage=before.content
            afterMessage=after.content
            embed=discord.Embed(title=author.name+"#"+author.discriminator, description="✏️ Messaggio modificato", color=0x00ff11)
            embed.add_field(name="prima", value="```"+beforeMessage+"```", inline=False)
            embed.add_field(name="dopo", value="```"+afterMessage+"```", inline=False)
            await self.edit_message_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        embed=discord.Embed(title="**"+member.name+"**#"+member.discriminator, description=member.name+" è stato bannato dal server!", color=0xff0000)
        embed.set_thumbnail(url=member.avatar)
        if self.ban_log_channel is not None:
            await self.ban_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        embed=discord.Embed(title="**"+member.name+"**#"+member.discriminator, description=member.name+" è stato sbannato dal server!", color=0x00ff11)
        embed.set_thumbnail(url=member.avatar)
        if self.ban_log_channel is not None:
            await self.unban_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        embed=discord.Embed(title="**"+member.name+"**#"+member.discriminator)
        embed.set_thumbnail(url=member.avatar)
        if self.voice_log_channel is not None:
            if before.channel is None and after.channel is not None:          
                embed.description=member.name + " è entrato in "+ after.channel.mention
                embed.color=0x00ff11
                await self.voice_log_channel.send(embed=embed)
            elif after.channel is None:
                embed.description=member.name + " è uscito da "+ before.channel.mention
                embed.color=0xff0000
                await self.voice_log_channel.send(embed=embed)
            elif after.channel != before.channel:
                embed.description=member.name + " è passato da "+ before.channel.mention + " a "+after.channel.mention
                embed.color=0x00ff11
                await self.voice_log_channel.send(embed=embed)


    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        self.welcome_channel = channel
        await ctx.send(f"Canale di benvenuto impostato su {channel.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_goodbye_channel(self, ctx, channel: discord.TextChannel):
        self.goodbye_channel = channel
        await ctx.send(f"Canale di addio impostato su {channel.mention}")

    @commands.has_permissions(administrator=True)  
    @commands.command()
    async def set_log_channel(self, ctx, channel: discord.TextChannel):
        self.log_channel = channel
        self.join_log_channel=self.log_channel
        self.leave_log_channel=self.log_channel
        self.edit_message_log_channel=self.log_channel
        self.delete_message_log_channel=self.log_channel
        self.ban_log_channel=self.log_channel
        self.unban_log_channel=self.log_channel
        self.voice_log_channel=self.log_channel
        await ctx.send(f"Canale di log impostato su {channel.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_join_log_channel(self, ctx, channel: discord.TextChannel):
        self.join_log_channel = channel
        await ctx.send(f"Canale log degli ingressi impostato su {channel.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_leave_log_channel(self, ctx, channel: discord.TextChannel):
        self.leave_log_channel = channel
        await ctx.send(f"Canale log delle uscite impostato su {channel.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_ban_log_channel(self, ctx, channel: discord.TextChannel):
        self.ban_log_channel = channel
        await ctx.send(f"Canale log dei ban impostato su {channel.mention}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_unban_log_channel(self, ctx, channel: discord.TextChannel):
        self.unban_log_channel = channel
        await ctx.send(f"Canale log degli unban impostato su {channel.mention}")

async def setup(bot):
    await bot.add_cog(ServerLogger(bot))