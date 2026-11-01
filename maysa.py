
import discord
from discord.ext import commands
import os
import random
from keep_alive import keep_alive

# AYARLAR
TOKEN = os.getenv("TOKEN")

AUTO_ROLE_ID = 1561154510641037362
LOG_CHANNEL_ID = 1561158414631964872
KOLE_USER_ID = 983769091485605888

# INTENTS
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# BOT AÇILDIĞINDA
@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Maysa <3")
    )
    print(f"{bot.user} aktif!")


# LOG GÖNDERME
async def send_log(guild, embed):
    channel = guild.get_channel(LOG_CHANNEL_ID)

    if channel:
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            print("Log kanalına mesaj gönderme yetkim yok!")
    else:
        print("Log kanalı bulunamadı!")


# ÜYE GİRİŞ
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)

    if role:
        try:
            await member.add_roles(role, reason="Otomatik giriş rolü")
        except discord.Forbidden:
            print("Otomatik rol verilemedi!")
        except discord.HTTPException as e:
            print(f"Rol hatası: {e}")

    embed = discord.Embed(
        title="📥 Sunucuya Giriş",
        description=f"{member.mention} sunucuya katıldı.",
        color=discord.Color.green()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Kullanıcı", value=member.name, inline=True)
    embed.add_field(name="ID", value=str(member.id), inline=True)
    embed.set_footer(text="Maysa Bot • Giriş Sistemi")

    await send_log(member.guild, embed)


# ÜYE ÇIKIŞ
@bot.event
async def on_member_remove(member):
    embed = discord.Embed(
        title="📤 Sunucudan Çıkış",
        description=f"**{member.name}** sunucudan ayrıldı.",
        color=discord.Color.red()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Kullanıcı", value=member.name, inline=True)
    embed.add_field(name="ID", value=str(member.id), inline=True)
    embed.set_footer(text="Maysa Bot • Çıkış Sistemi")

    await send_log(member.guild, embed)


# YARDIM
@bot.command()
async def yardım(ctx):
    embed = discord.Embed(
        title="Maysa • Yardım Menüsü",
        description="Bot komutları aşağıda listelenmiştir.",
        color=discord.Color.pink()
    )

    embed.add_field(
        name="Genel",
        value="`!ping` `!avatar` `!sunucu` `!kullanıcı` `!kaçkişi`",
        inline=False
    )
    embed.add_field(
        name="Eğlence",
        value="`!kaçyaş` `!zar` `!yazitura` `!rastgele` `!8ball` `!ters` `!ship` `!oylama`",
        inline=False
    )
    embed.add_field(
        name="Yetkili",
        value="`!temizle` `!sil` `!yaz` `!köle` `!ban` `!kick`",
        inline=False
    )

    await ctx.send(embed=embed)


# PING
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")


# AVATAR
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title=f"{member.name} • Avatar",
        color=discord.Color.blurple()
    )
    embed.set_image(url=member.display_avatar.url)

    await ctx.send(embed=embed)


# SUNUCU BİLGİSİ
@bot.command()
async def sunucu(ctx):
    guild = ctx.guild

    embed = discord.Embed(
        title=guild.name,
        color=discord.Color.blurple()
    )
    embed.add_field(name="Üye Sayısı", value=guild.member_count)
    embed.add_field(name="Sunucu ID", value=guild.id)
    embed.add_field(name="Kuruluş", value=discord.utils.format_dt(guild.created_at, "D"))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    await ctx.send(embed=embed)


# KULLANICI BİLGİSİ
@bot.command()
async def kullanıcı(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title="Kullanıcı Bilgisi",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="İsim", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Hesap Oluşturma", value=discord.utils.format_dt(member.created_at, "D"))
    embed.add_field(name="Sunucuya Katılma", value=discord.utils.format_dt(member.joined_at, "D") if member.joined_at else "Bilinmiyor")

    await ctx.send(embed=embed)


# KAÇ KİŞİ
@bot.command()
async def kaçkişi(ctx):
    await ctx.send(f"👥 Sunucuda toplam **{ctx.guild.member_count}** kişi var.")


# KAÇ YAŞ
@bot.command()
async def kaçyaş(ctx, member: discord.Member = None):
    member = member or ctx.author
    gun = (discord.utils.utcnow() - member.created_at).days

    await ctx.send(f"📅 {member.mention} hesabı **{gun} günlük**.")


# ZAR
@bot.command()
async def zar(ctx):
    await ctx.send(f"🎲 Gelen sayı: **{random.randint(1, 6)}**")


# YAZI TURA
@bot.command()
async def yazitura(ctx):
    await ctx.send(f"🪙 **{random.choice(['Yazı', 'Tura'])}**")


# RASTGELE
@bot.command()
async def rastgele(ctx, maksimum: int = 100):
    if maksimum < 1:
        return await ctx.send("En az 1 yazmalısın!")

    await ctx.send(f"🎯 Sonuç: **{random.randint(1, maksimum)}**")


# 8BALL
@bot.command(name="8ball")
async def eightball(ctx, *, soru: str):
    cevaplar = [
        "Kesinlikle!",
        "Bence evet.",
        "Olabilir.",
        "Hiç sanmıyorum.",
        "Bunu zaman gösterecek.",
        "Kesinlikle hayır!"
    ]

    await ctx.send(f"🎱 {random.choice(cevaplar)}")


# TERS
@bot.command()
async def ters(ctx, *, mesaj: str):
    await ctx.send(mesaj[::-1])


# SHIP
@bot.command()
async def ship(ctx, uye1: discord.Member, uye2: discord.Member):
    oran = random.randint(0, 100)

    await ctx.send(
        f"💗 {uye1.mention} + {uye2.mention}\n"
        f"Uyum oranı: **%{oran}**"
    )


# OYLAMA
@bot.command()
async def oylama(ctx, *, soru: str):
    mesaj = await ctx.send(f"📊 **{soru}**\n\n👍 Evet\n👎 Hayır")
    await mesaj.add_reaction("👍")
    await mesaj.add_reaction("👎")


# TEMİZLE
@bot.command()
@commands.has_permissions(manage_messages=True)
async def temizle(ctx, miktar: int):
    if miktar < 1 or miktar > 100:
        return await ctx.send("1 ile 100 arasında bir sayı yazmalısın.")

    silinen = await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f"🧹 {len(silinen) - 1} mesaj silindi.", delete_after=3)


# SİL
@bot.command()
@commands.has_permissions(manage_messages=True)
async def sil(ctx, miktar: int = 1):
    if miktar < 1 or miktar > 100:
        return await ctx.send("1 ile 100 arasında bir sayı yazmalısın.")

    silinen = await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f"🧹 {len(silinen) - 1} mesaj silindi.", delete_after=3)


# YAZ
@bot.command()
@commands.has_permissions(manage_messages=True)
async def yaz(ctx, *, mesaj: str):
    await ctx.send(mesaj)


# KÖLE
@bot.command()
async def köle(ctx):
    await ctx.send(f"<@{KOLE_USER_ID}>")


# BAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, sebep="Sebep belirtilmedi"):
    await member.ban(reason=sebep)
    await ctx.send(f"🔨 {member.mention} banlandı. Sebep: {sebep}")


# KICK
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, sebep="Sebep belirtilmedi"):
    await member.kick(reason=sebep)
    await ctx.send(f"👢 {member.mention} sunucudan atıldı. Sebep: {sebep}")


# HATA YÖNETİMİ
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Gerekli bir bilgiyi eksik girdin.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu komutu kullanmak için yetkin yok.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Geçersiz kullanıcı veya sayı girdin.")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        print(f"Komut hatası: {error}")


# BOTU BAŞLAT
keep_alive()
bot.run(TOKEN)

