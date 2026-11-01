
import discord
from discord.ext import commands
import os
import random
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="Maysa ❤️ 1223")
    )


# YARDIM
@bot.command(name="yardım")
async def yardim(ctx):
    embed = discord.Embed(title="🤖 MAYSA BOT KOMUTLARI", color=discord.Color.blurple())
    embed.add_field(name="📌 Genel", value=(
        "`!ping` `!avatar` `!sunucu`\n"
        "`!kullanıcı` `!kaçkişi` `!kaçyaş`"
    ), inline=False)
    embed.add_field(name="🎮 Eğlence", value=(
        "`!zar` `!yazitura` `!rastgele 100`\n"
        "`!8ball soru` `!ship @kişi @kişi`\n"
        "`!ters mesaj` `!oylama soru` `!kaçcm @kişi`"
    ), inline=False)
    embed.add_field(name="🛡️ Moderasyon", value=(
        "`!ban @kişi sebep`\n"
        "`!kick @kişi sebep`\n"
        "`!temizle 10` `!sil 5`"
    ), inline=False)
    embed.add_field(name="💬 Diğer", value="`!yaz mesaj` `!sik`", inline=False)
    await ctx.send(embed=embed)


# PING
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")


# AVATAR
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member} - Avatar", color=discord.Color.blurple())
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)


# SUNUCU
@bot.command()
async def sunucu(ctx):
    g = ctx.guild
    embed = discord.Embed(title=g.name, color=discord.Color.blue())
    embed.add_field(name="Üye Sayısı", value=g.member_count)
    embed.add_field(name="Kanal Sayısı", value=len(g.channels))
    embed.add_field(name="Sunucu Sahibi", value=g.owner.mention)
    embed.add_field(name="Oluşturulma", value=g.created_at.strftime("%d.%m.%Y"))
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await ctx.send(embed=embed)


# KULLANICI
@bot.command()
async def kullanıcı(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="Kullanıcı Bilgileri", color=discord.Color.green())
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Kullanıcı", value=member.mention)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Hesap Tarihi", value=member.created_at.strftime("%d.%m.%Y"))
    if member.joined_at:
        embed.add_field(name="Katılma Tarihi", value=member.joined_at.strftime("%d.%m.%Y"))
    await ctx.send(embed=embed)


# KAÇ KİŞİ
@bot.command()
async def kaçkişi(ctx):
    await ctx.send(f"👥 Sunucuda **{ctx.guild.member_count}** kişi var.")


# KAÇ YAŞ
@bot.command()
async def kaçyaş(ctx):
    gün = (discord.utils.utcnow() - ctx.author.created_at).days
    await ctx.send(f"🗓️ Discord hesabın **{gün} gündür** açık!")


# ZAR
@bot.command()
async def zar(ctx):
    await ctx.send(f"🎲 Sonuç: **{random.randint(1, 6)}**")


# YAZI TURA
@bot.command()
async def yazitura(ctx):
    await ctx.send(f"🪙 **{random.choice(['Yazı', 'Tura'])}**")


# RASTGELE SAYI
@bot.command()
async def rastgele(ctx, maksimum: int = 100):
    if maksimum < 1 or maksimum > 1000000:
        await ctx.send("1 ile 1000000 arasında sayı gir.")
        return
    await ctx.send(f"🎲 Rastgele sayı: **{random.randint(1, maksimum)}**")


# 8BALL
@bot.command(name="8ball")
async def eightball(ctx, *, soru=None):
    if not soru:
        await ctx.send("Bir soru yazmalısın.")
        return
    cevaplar = [
        "Kesinlikle evet ❤️", "Bence evet.", "Olabilir.",
        "Zaman gösterecek.", "Pek sanmıyorum.",
        "Kesinlikle hayır.", "Şansını tekrar dene."
    ]
    await ctx.send(f"🎱 {random.choice(cevaplar)}")


# TERS MESAJ
@bot.command()
async def ters(ctx, *, mesaj):
    await ctx.send(mesaj[::-1])


# SHIP
@bot.command()
async def ship(ctx, kisi1: discord.Member, kisi2: discord.Member):
    puan = random.randint(0, 100)
    embed = discord.Embed(
        title="❤️ Uyum Testi",
        description=f"{kisi1.mention} + {kisi2.mention}\n\n**Uyum: %{puan}**",
        color=discord.Color.magenta()
    )
    await ctx.send(embed=embed)


# KAÇ CM
@bot.command()
async def kaçcm(ctx, member: discord.Member = None):
    member = member or ctx.author
    cm = random.randint(1, 30)
    await ctx.send(f"📏 {member.mention} için tamamen rastgele sonuç: **{cm} cm** 😂")


# OYLAMA
@bot.command()
@commands.has_permissions(manage_messages=True)
async def oylama(ctx, *, soru):
    embed = discord.Embed(
        title="📊 OYLAMA",
        description=f"**{soru}**\n\n👍 Evet\n👎 Hayır",
        color=discord.Color.blurple()
    )
    embed.set_footer(text=f"Başlatan: {ctx.author}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")


# TEMİZLE
@bot.command()
@commands.has_permissions(manage_messages=True)
async def temizle(ctx, miktar: int):
    if not 1 <= miktar <= 100:
        await ctx.send("1-100 arasında sayı gir.")
        return
    silinen = await ctx.channel.purge(limit=miktar + 1)
    mesaj = await ctx.send(f"🧹 {len(silinen) - 1} mesaj silindi.")
    await mesaj.delete(delay=3)


# SİL - KOMUT DAHİL SON MESAJLARI SİLER
@bot.command()
@commands.has_permissions(manage_messages=True)
async def sil(ctx, miktar: int = 1):
    if not 1 <= miktar <= 100:
        await ctx.send("1-100 arasında sayı gir.")
        return
    silinen = await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f"🗑️ {len(silinen) - 1} mesaj silindi.", delete_after=3)


# YAZ
@bot.command()
async def yaz(ctx, *, mesaj):
    await ctx.send(mesaj)


# SIK
@bot.command()
async def sik(ctx):
    await ctx.send("siktim")


# BAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} banlandı. Sebep: {reason or 'Belirtilmedi'}")


# KICK
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} sunucudan atıldı.")


# HATA YÖNETİMİ
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu komut için yetkin yok!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Gerekli bilgileri girmedin.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Kullanıcı bulunamadı.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Hatalı kullanım.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"Hata: {error}")


bot.run(os.getenv("TOKEN"))
