# Import the following modules
import asyncio
from captcha.image import ImageCaptcha
from discord.ext import commands
import random
import string
import discord

class Verify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.verifying_users = set()

    @staticmethod
    def generate_captcha_str():
        captcha_chars = string.ascii_letters + string.digits
        captcha = ''.join(random.sample(captcha_chars, 6))
        return captcha

    @staticmethod    
    def generate_captcha():
            # Create an image instance of the given size
            image = ImageCaptcha(width = 280, height = 90)   
            # Image captcha text
            captcha_text = Verify.generate_captcha_str()        
            # generate the image of the given text
            data = image.generate(captcha_text) 
            image.write(captcha_text, 'captcha.png')
            return captcha_text

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id==1065665084854128753:
            #Rimuove l'emoji messa dall'utente che si sta verificando
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, self.bot.get_user(payload.user_id))

            #Controlla se l'utente si sta già verificando. Se è così, ritorna. 
            # Altrimenti, aggiunge l'utente alla lista di quelli che si stanno verificando
            user_id = payload.user_id
            if user_id in self.verifying_users:
                return 
            self.verifying_users.add(user_id)

            user = self.bot.get_user(user_id)
            if payload.emoji.name == "✅" and payload.channel_id == 1065665084854128753:
                user = self.bot.get_user(payload.user_id)
                # genera un captcha
                captcha = Verify.generate_captcha()
                # invia il captcha al nuovo utente
                await user.send("Risolvi il captcha se vuoi diventare una bestia 🦍", file=discord.File("captcha.png"))
                # chiede la risposta del captcha all'utente
                try:
                    response = await self.bot.wait_for("message", check=lambda message: message.author == user, timeout=60)
                except asyncio.TimeoutError:
                    await user.send("Tempo scaduto! Non sei stato verificato 😡")
                    return
                # controlla se la risposta è corretta
                if response.content.lower() != captcha.lower():
                    await user.send("❌ Captcha errato! Non sei stato verificato 😡")
                else:
                    await user.send("✅ Captcha corretto! Sei stato verificato 🦍")
                    # assegna il ruolo di verifica all'utente
                    role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name="Bestia®")
                    member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
                    await member.add_roles(role)
                self.verifying_users.remove(user_id)

async def setup(bot):
    await bot.add_cog(Verify(bot))