import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# Web sunucusunu başlat (UptimeRobot için keep-alive)
keep_alive()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Ses kanalları için şart

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")
    
    # 1. DURUM MESAJI
    activity = discord.Game(name="Maysa'yı Seviyor ❤️")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    
    # 2. SES KANALINA BAĞLANMA (Sürekli durması için)
    CHANNEL_ID = 1565561538314772540  # <--- Kendi ses kanalının ID'sini buraya yaz!
    
    channel = bot.get_channel(1565561538314772540)
    if channel:
        try:
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                await channel.connect()
                print(f"Başarıyla {channel.name} ses kanalına girildi ve sabitlendi!")
        except Exception as e:
            print(f"Sese bağlanırken hata oluştu: {e}")
    else:
        print("Kanal bulunamadı! ID'yi kontrol et.")

# --- KOMUTLAR ---

# 1. !sik -> cevap: siktim
@bot.command()
async def sik(ctx):
    await ctx.send("siktim")

# 2. !ban @kullanici sebep
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("Bunu yapmak için yetkin yok!")
        return
    
    try:
        await member.ban(reason=reason)
        await ctx.send(f"Başarıyla banlandı: {member.mention} (Sebep: {reason or 'Belirtilmedi'})")
    except Exception as e:
        await ctx.send(f"Banlanırken bir hata oluştu: {e}")

# 3. !kick @kullanici sebep
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("Bunu yapmak için yetkin yok!")
        return
    
    try:
        await member.kick(reason=reason)
        await ctx.send(f"Başarıyla atıldı (kick): {member.mention} (Sebep: {reason or 'Belirtilmedi'})")
    except Exception as e:
        await ctx.send(f"Atılırken bir hata oluştu: {e}")

# Render için gizli token çekme kısmı
bot.run(os.getenv("TOKEN"))