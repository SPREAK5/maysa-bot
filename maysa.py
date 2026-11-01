
import discord
from discord.ext import commands
import os
import random
from keep_alive import keep_alive

# AYARLAR
TOKEN = os.getenv("TOKEN")
AUTO_ROLE_ID = 1561154510641037362
KOLE_USER_ID = 983769091485605888

keep_alive()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# BOT AÇILDIĞINDA
@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="Maysa <3")
    )


# ÜYE GİRİŞİ
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)

    if role:
        try:
            await member.add_roles(role, reason="Otomatik giriş rolü")
            print(f"{member} kullanıcısına rol verildi.")
        except discord.Forbidden:
            print("Rol verilemedi. Bot rolünü kontrol et.")
        except discord.HTTPException as error:
            print(f"Rol hatası: {error}")
    else:
        print("Otomatik rol bulunamadı!")

    channel = member.guild.system_channel
    if channel:
        await channel.send(f"👋 Hoş geldin {member.mention}! ❤️")


# ÜYE ÇIKIŞI
@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"👋 {member.name} sunucudan ayrıldı.")


# YARDIM
@bot.command(name="yardım")
async def yardim(ctx):
    embed = discord.Embed(
        title="🤖 MAYSA BOT KOMUTLARI",
        color=discord.Color.blurple()
    )
    embed.add_field(
        name="📌 Genel",
        value="`!ping` `!avatar` `!sunucu` `!kullanıcı` `!kaçkişi` `!kaçyaş`",
        inline=False
    )
    embed.add_field(
        name="🎮 Eğlence",
        value="`!zar` `!yazitura` `!rastgele 100` `!8ball soru` `!ters mesaj` `!ship @kişi @kişi`",
        inline=False
    )
    embed.add_field(
        name="🛡️ Moderasyon",
        value="`!ban @kişi sebep` `!kick @kişi sebep` `!sil 5` `!temizle 10` `!oylama soru`",
        inline=False
    )
    embed.add_field(
        name="💬 Diğer",
        value="`!yaz mesaj` `!köle`",
        inline=False
    )
    await ctx.send(embed=embed)


# PING
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")


# AVATAR
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member} - Avatar")
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)


# SUNUCU
@bot.command()
async def sunucu(ctx):
    g = ctx.guild
    embed = discord.Embed(title=g.name, color=discord.Color.blue())
    embed.add_field(name="Üye Sayısı", value=g.member_count)
    embed.add_field(name="Kanal Sayısı", value=len(g.channels))
    embed.add_field(name="Sunucu Sahibi", value=str(g.owner))
    embed.add_field(name="Kuruluş", value=g.created_at.strftime("%d.%m.%Y"))
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await ctx.send(embed=embed)


# KULLANICI
@bot.command()
async def kullanıcı(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="Kullanıcı Bilgileri")
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
    await ctx.send(f"👥 Sunucuda {ctx.guild.member_count} kişi var.")


# KAÇ YAŞ
@bot.command()
async def kaçyaş(ctx):
    gün = (discord.utils.utcnow() - ctx.author.created_at).days
    await ctx.send(f"🗓️ Discord hesabın {gün} gündür açık!")


# ZAR
@bot.command()
async def zar(ctx):
    await ctx.send(f"🎲 {random.randint(1, 6)}")


# YAZI TURA
@bot.command()
async def yazitura(ctx):
    await ctx.send(f"🪙 {random.choice(['Yazı', 'Tura'])}")


# RASTGELE
@bot.command()
async def rastgele(ctx, maksimum: int = 100):
    if not 1 <= maksimum <= 1000000:
        await ctx.send("1 ile 1000000 arasında sayı gir.")
        return
    await ctx.send(f"🎲 {random.randint(1, maksimum)}")


# 8BALL
@bot.command(name="8ball")
async def eightball(ctx, *, soru=None):
    if not soru:
        await ctx.send("Bir soru yazmalısın.")

    else:
        cevaplar = [
            "Kesinlikle evet ❤️",
            "Bence evet.",
            "Olabilir.",
            "Zaman gösterecek.",
            "Pek sanmıyorum.",
            "Kesinlikle hayır."
        ]
        await ctx.send(f"🎱 {random.choice(cevaplar)}")


# TERS
@bot.command()
async def ters(ctx, *, mesaj):
    await ctx.send(mesaj[::-1])


# SHIP
@bot.command()
async def ship(ctx, kisi1: discord.Member, kisi2: discord.Member):
    puan = random.randint(0, 100)
    await ctx.send(
        f"❤️ {kisi1.mention} + {kisi2.mention}\nUyum puanı: **%{puan}**"
    )


# OYLAMA
@bot.command()
@commands.has_permissions(manage_messages=True)
async def oylama(ctx, *, soru):
    embed = discord.Embed(
        title="📊 OYLAMA",
        description=f"{soru}\n\n👍 Evet\n👎 Hayır",
        color=discord.Color.blurple()
    )
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


# SİL
@bot.command()
@commands.has_permissions(manage_messages=True)
async def sil(ctx, miktar: int = 1):
    if not 1 <= miktar <= 100:
        await ctx.send("1-100 arasında sayı gir.")
        return

    silinen = await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(
        f"🗑️ {len(silinen) - 1} mesaj silindi.",
        delete_after=3
    )


# YAZ
@bot.command()
async def yaz(ctx, *, mesaj):
    await ctx.send(mesaj)


# KÖLE
@bot.command(name="köle")
async def kole(ctx):
    await ctx.send(f"<@{KOLE_USER_ID}>")


# BAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Belirtilmedi"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} banlandı. Sebep: {reason}")


# KICK
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Belirtilmedi"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} sunucudan atıldı.")


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
        print(f"Komut hatası: {repr(error)}")


if not TOKEN:
    raise RuntimeError("TOKEN bulunamadı! Render Environment Variables bölümünü kontrol et.")

bot.run(TOKEN)

