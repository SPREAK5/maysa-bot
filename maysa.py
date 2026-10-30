import keep_alive
keep_alive.keep_alive()

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot başarıyla giriş yaptı: {bot.user}")

@bot.command()
async def merhaba(ctx):
    await ctx.send(f"Selamlar {ctx.author.name}! Bot aktif ve çalışıyor :rocket:")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def sil(ctx, miktar: int):
    await ctx.message.delete()
    silinen = await ctx.channel.purge(limit=miktar)
    await ctx.send(f":broom: Başarıyla **{len(silinen)}** adet mesaj silindi!", delete_after=5)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, sebep="Sebep belirtilmedi"):
    await member.ban(reason=sebep)
    await ctx.send(f":hammer: **{member.name}** sunucudan yasaklandı! Sebep: *{sebep}*")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, sebep="Sebep belirtilmedi"):
    await member.kick(reason=sebep)
    await ctx.send(f":boot: **{member.name}** sunucudan atıldı! Sebep: *{sebep}*")

@sil.error
@ban.error
@kick.error
async def komut_hatasi(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":x: Üzgünüm, bu komutu kullanmak için yeterli yetkiye sahip değilsin!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":x: Eksik parametre girdin! Komutu doğru kullandığından emin ol (Örn: `!sil 5`)")

bot.run("")