#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import os
import json
import random
import asyncio
from dotenv import load_dotenv
from keep_alive import keep_alive

keep_alive()    

# تحميل متغيرات البيئة
load_dotenv()

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ملف لحفظ إعدادات القنوات
CHANNELS_FILE = 'active_channels.json'

# قاموس الردود العربية مع الإيموجي
ARABIC_RESPONSES = {
    'greetings': [
        'أهلاً وسهلاً! 👋',
        'مرحباً بك! 😊',
        'السلام عليكم ورحمة الله وبركاته! 🌟',
        'أهلاً بك في الخادم! 🎉',
        'مرحباً! كيف حالك اليوم؟ 😄'
    ],
    'thanks': [
        'العفو! 😊',
        'لا شكر على واجب! 💙',
        'أهلاً وسهلاً! 🌟',
        'دائماً في الخدمة! 👍',
        'بالتوفيق! ✨'
    ],
    'good_morning': [
        'صباح الخير! ☀️',
        'صباح النور! 🌅',
        'صباحك سعيد! 😊',
        'أسعد الله صباحك! 🌸',
        'صباح الورد! 🌹'
    ],
    'good_evening': [
        'مساء الخير! 🌙',
        'مساء النور! ⭐',
        'مساءك سعيد! 😊',
        'أسعد الله مساءك! 🌆',
        'مساء الورد! 🌺'
    ],
    'encouragement': [
        'أحسنت! 👏',
        'ممتاز! 🌟',
        'رائع جداً! 🎉',
        'واصل التميز! 💪',
        'أنت مبدع! ✨'
    ],
    'help': [
        'كيف يمكنني مساعدتك؟ 🤔',
        'أنا هنا للمساعدة! 💙',
        'ما الذي تحتاج إليه؟ 😊',
        'تفضل، كيف أساعدك؟ 🙋‍♂️'
    ]
}

# كلمات مفتاحية للتفاعل
KEYWORDS = {
    'greetings': ['مرحبا', 'أهلا', 'السلام عليكم', 'هلا', 'اهلين', 'مرحباً', 'أهلاً'],
    'thanks': ['شكرا', 'شكراً', 'مشكور', 'يعطيك العافية', 'الله يعطيك العافية'],
    'good_morning': ['صباح الخير', 'صباح النور', 'صباحكم خير'],
    'good_evening': ['مساء الخير', 'مساء النور', 'مساءكم خير'],
    'encouragement': ['أحسنت', 'ممتاز', 'رائع', 'جميل', 'مبدع'],
    'help': ['مساعدة', 'ساعدني', 'أحتاج مساعدة', 'كيف']
}

def load_active_channels():
    """تحميل قائمة القنوات النشطة"""
    try:
        with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_active_channels(channels):
    """حفظ قائمة القنوات النشطة"""
    with open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
        json.dump(channels, f, ensure_ascii=False, indent=2)

# متغير لحفظ القنوات النشطة
active_channels = load_active_channels()

@bot.event
async def on_ready():
    """عند تشغيل البوت"""
    print(f'🤖 البوت {bot.user} جاهز للعمل!')
    print(f'📊 متصل بـ {len(bot.guilds)} خادم')
    
    # تعيين حالة البوت
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="الرسائل العربية 👀"
        )
    )

@bot.event
async def on_message(message):
    """التعامل مع الرسائل"""
    # تجاهل رسائل البوت نفسه
    if message.author == bot.user:
        return
    
    # التحقق من أن القناة نشطة
    guild_id = str(message.guild.id) if message.guild else 'dm'
    channel_id = str(message.channel.id)
    
    if guild_id in active_channels and channel_id not in active_channels[guild_id]:
        # القناة غير نشطة، لا تتفاعل
        await bot.process_commands(message)
        return
    
    # إذا لم يتم تحديد قنوات نشطة، تفاعل في جميع القنوات
    if guild_id not in active_channels:
        active_channels[guild_id] = []
    
    # التفاعل مع الرسائل العربية
    content = message.content.lower()
    
    # البحث عن كلمات مفتاحية والرد عليها
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in content:
                response = random.choice(ARABIC_RESPONSES[category])
                await message.channel.send(response)
                break
        else:
            continue
        break
    
    # معالجة الأوامر
    await bot.process_commands(message)

@bot.command(name='مرحبا', aliases=['اهلا', 'هلا'])
async def hello_command(ctx):
    """أمر الترحيب"""
    response = random.choice(ARABIC_RESPONSES['greetings'])
    await ctx.send(f'{response} {ctx.author.mention}')

@bot.command(name='مساعدة', aliases=['help_ar'])
async def help_arabic(ctx):
    """عرض قائمة الأوامر بالعربية"""
    embed = discord.Embed(
        title="🤖 أوامر البوت العربي",
        description="قائمة بجميع الأوامر المتاحة",
        color=0x00ff00
    )
    
    embed.add_field(
        name="🎯 الأوامر الأساسية",
        value="""
        `!مرحبا` - ترحيب
        `!مساعدة` - عرض هذه القائمة
        `!حالة` - عرض حالة البوت
        `!تفعيل_القناة` - تفعيل التفاعل في هذه القناة
        `!إلغاء_القناة` - إلغاء التفاعل في هذه القناة
        `!القنوات_النشطة` - عرض القنوات النشطة
        """,
        inline=False
    )
    
    embed.add_field(
        name="💬 التفاعل التلقائي",
        value="البوت يتفاعل تلقائياً مع الكلمات العربية مثل: مرحبا، شكراً، صباح الخير، مساء الخير",
        inline=False
    )
    
    embed.set_footer(text="البوت العربي التفاعلي 🇸🇦")
    
    await ctx.send(embed=embed)

@bot.command(name='حالة')
async def status_command(ctx):
    """عرض حالة البوت"""
    embed = discord.Embed(
        title="📊 حالة البوت",
        color=0x0099ff
    )
    
    embed.add_field(name="🟢 الحالة", value="متصل وجاهز", inline=True)
    embed.add_field(name="📡 زمن الاستجابة", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="🏠 الخوادم", value=len(bot.guilds), inline=True)
    embed.add_field(name="👥 المستخدمين", value=len(bot.users), inline=True)
    
    guild_id = str(ctx.guild.id)
    active_count = len(active_channels.get(guild_id, []))
    embed.add_field(name="📺 القنوات النشطة", value=active_count, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='تفعيل_القناة')
@commands.has_permissions(manage_channels=True)
async def activate_channel(ctx):
    """تفعيل التفاعل في القناة الحالية"""
    guild_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)
    
    if guild_id not in active_channels:
        active_channels[guild_id] = []
    
    if channel_id not in active_channels[guild_id]:
        active_channels[guild_id].append(channel_id)
        save_active_channels(active_channels)
        await ctx.send(f"✅ تم تفعيل التفاعل في قناة {ctx.channel.mention}")
    else:
        await ctx.send(f"ℹ️ القناة {ctx.channel.mention} مفعلة مسبقاً")

@bot.command(name='إلغاء_القناة')
@commands.has_permissions(manage_channels=True)
async def deactivate_channel(ctx):
    """إلغاء التفاعل في القناة الحالية"""
    guild_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)
    
    if guild_id in active_channels and channel_id in active_channels[guild_id]:
        active_channels[guild_id].remove(channel_id)
        save_active_channels(active_channels)
        await ctx.send(f"❌ تم إلغاء التفاعل في قناة {ctx.channel.mention}")
    else:
        await ctx.send(f"ℹ️ القناة {ctx.channel.mention} غير مفعلة")

@bot.command(name='القنوات_النشطة')
async def list_active_channels(ctx):
    """عرض قائمة القنوات النشطة"""
    guild_id = str(ctx.guild.id)
    
    if guild_id not in active_channels or not active_channels[guild_id]:
        await ctx.send("📭 لا توجد قنوات نشطة حالياً")
        return
    
    embed = discord.Embed(
        title="📺 القنوات النشطة",
        description="قائمة القنوات التي يتفاعل فيها البوت",
        color=0x00ff00
    )
    
    channels_list = []
    for channel_id in active_channels[guild_id]:
        channel = bot.get_channel(int(channel_id))
        if channel:
            channels_list.append(f"• {channel.mention}")
    
    if channels_list:
        embed.add_field(
            name="القنوات:",
            value="\n".join(channels_list),
            inline=False
        )
    else:
        embed.add_field(
            name="تنبيه:",
            value="لا توجد قنوات صالحة في القائمة",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """التعامل مع أخطاء الأوامر"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ ليس لديك الصلاحيات المطلوبة لتنفيذ هذا الأمر")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ أمر غير معروف. استخدم `!مساعدة` لعرض قائمة الأوامر")
    else:
        print(f"خطأ: {error}")
        await ctx.send("❌ حدث خطأ أثناء تنفيذ الأمر")

# تحميل الإضافات
async def load_extensions():
    """تحميل جميع الإضافات"""
    try:
        await bot.load_extension('advanced_commands')
        print("✅ تم تحميل الأوامر المتقدمة")
        
        await bot.load_extension('channel_manager')
        print("✅ تم تحميل مدير القنوات")
    except Exception as e:
        print(f"❌ خطأ في تحميل الإضافات: {e}")

# تشغيل البوت
async def main():
    """الدالة الرئيسية لتشغيل البوت"""
    await load_extensions()
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ خطأ: لم يتم العثور على توكن البوت في ملف .env")
        print("يرجى إضافة DISCORD_TOKEN=your_token_here في ملف .env")
        return
    
    try:
        await bot.start(token)
    except discord.LoginFailure:
        print("❌ خطأ في تسجيل الدخول: تحقق من صحة التوكن")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

if __name__ == "__main__":
    asyncio.run(main())

