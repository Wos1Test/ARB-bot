#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime
from responses import ArabicResponses, get_random_emoji

class AdvancedCommands(commands.Cog):
    """فئة الأوامر المتقدمة للبوت العربي"""
    
    def __init__(self, bot):
        self.bot = bot
        self.user_interactions = {}  # لتتبع تفاعلات المستخدمين
    
    @commands.command(name='وقت', aliases=['الوقت', 'الساعة'])
    async def current_time(self, ctx):
        """عرض الوقت الحالي مع تحية مناسبة"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        
        # تحية حسب الوقت
        greeting = ArabicResponses.get_time_based_response()
        
        embed = discord.Embed(
            title="🕐 الوقت الحالي",
            color=0x3498db
        )
        embed.add_field(name="⏰ الساعة", value=time_str, inline=True)
        embed.add_field(name="📅 التاريخ", value=date_str, inline=True)
        embed.add_field(name="💬 تحية", value=greeting, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='تحفيز', aliases=['حماس', 'دافع'])
    async def motivation(self, ctx):
        """إرسال رسالة تحفيزية"""
        response = ArabicResponses.get_random_response('motivation')
        emoji = get_random_emoji('success')
        
        embed = discord.Embed(
            title=f"💪 رسالة تحفيزية {emoji}",
            description=response,
            color=0xe74c3c
        )
        embed.set_footer(text="أنت قادر على تحقيق المستحيل!")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='حكمة', aliases=['نصيحة', 'موعظة'])
    async def wisdom(self, ctx):
        """مشاركة حكمة أو نصيحة"""
        response = ArabicResponses.get_random_response('wisdom')
        emoji = get_random_emoji('wisdom')
        
        embed = discord.Embed(
            title=f"📚 حكمة اليوم {emoji}",
            description=response,
            color=0x9b59b6
        )
        embed.set_footer(text="الحكمة ضالة المؤمن")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='مزاج', aliases=['شعور', 'حالة_نفسية'])
    async def mood_check(self, ctx, *, mood=None):
        """التحقق من المزاج والرد المناسب"""
        if not mood:
            question = ArabicResponses.get_random_question()
            await ctx.send(f"{ctx.author.mention} {question}")
            return
        
        mood = mood.lower()
        
        # تحديد المشاعر حسب الكلمات
        if any(word in mood for word in ['سعيد', 'فرحان', 'مبسوط', 'رائع']):
            response = ArabicResponses.get_emotion_response('happy')
            color = 0x2ecc71
        elif any(word in mood for word in ['حزين', 'زعلان', 'مكتئب', 'تعبان']):
            response = ArabicResponses.get_emotion_response('sad')
            color = 0x3498db
        elif any(word in mood for word in ['متحمس', 'نشيط', 'حماسي', 'متفائل']):
            response = ArabicResponses.get_emotion_response('excited')
            color = 0xe67e22
        elif any(word in mood for word in ['متعب', 'مرهق', 'نعسان', 'كسلان']):
            response = ArabicResponses.get_emotion_response('tired')
            color = 0x95a5a6
        else:
            response = "أفهم مشاعرك، وأتمنى لك يوماً أفضل 💙"
            color = 0x9b59b6
        
        embed = discord.Embed(
            title="💭 حالتك النفسية",
            description=response,
            color=color
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='لعبة', aliases=['تسلية', 'ألعاب'])
    async def games(self, ctx, game_type=None):
        """ألعاب تفاعلية بسيطة"""
        if not game_type:
            embed = discord.Embed(
                title="🎮 الألعاب المتاحة",
                description="""
                `!لعبة تخمين` - لعبة تخمين الرقم
                `!لعبة سؤال` - أسئلة عامة
                `!لعبة حظ` - اختبار الحظ
                """,
                color=0xf39c12
            )
            await ctx.send(embed=embed)
            return
        
        if game_type == 'تخمين':
            await self.guessing_game(ctx)
        elif game_type == 'سؤال':
            await self.question_game(ctx)
        elif game_type == 'حظ':
            await self.luck_game(ctx)
    
    async def guessing_game(self, ctx):
        """لعبة تخمين الرقم"""
        number = random.randint(1, 10)
        await ctx.send("🎯 خمن رقماً بين 1 و 10! لديك 3 محاولات")
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        attempts = 3
        while attempts > 0:
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
                guess = int(msg.content)
                
                if guess == number:
                    await ctx.send(f"🎉 أحسنت! الرقم كان {number}")
                    return
                elif guess < number:
                    await ctx.send(f"📈 أعلى! المحاولات المتبقية: {attempts-1}")
                else:
                    await ctx.send(f"📉 أقل! المحاولات المتبقية: {attempts-1}")
                
                attempts -= 1
                
            except (ValueError, asyncio.TimeoutError):
                await ctx.send("❌ يرجى إدخال رقم صحيح أو انتهت المهلة الزمنية")
                return
        
        await ctx.send(f"😔 انتهت المحاولات! الرقم كان {number}")
    
    async def question_game(self, ctx):
        """لعبة الأسئلة العامة"""
        questions = [
            {"q": "ما هي عاصمة السعودية؟", "a": "الرياض"},
            {"q": "كم عدد أيام السنة؟", "a": "365"},
            {"q": "ما هو أكبر محيط في العالم؟", "a": "الهادئ"},
            {"q": "في أي قارة تقع مصر؟", "a": "أفريقيا"},
            {"q": "كم عدد ألوان قوس قزح؟", "a": "7"}
        ]
        
        question = random.choice(questions)
        await ctx.send(f"❓ {question['q']}")
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
            if question['a'].lower() in msg.content.lower():
                await ctx.send("🎉 إجابة صحيحة! أحسنت")
            else:
                await ctx.send(f"❌ إجابة خاطئة. الإجابة الصحيحة: {question['a']}")
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ انتهى الوقت! الإجابة كانت: {question['a']}")
    
    async def luck_game(self, ctx):
        """لعبة اختبار الحظ"""
        luck_results = [
            "🍀 حظك رائع اليوم!",
            "⭐ حظ جيد ينتظرك",
            "🌟 حظك متوسط، لكن الأمل موجود",
            "🎲 حظك متقلب اليوم",
            "💫 حظك في تحسن مستمر"
        ]
        
        result = random.choice(luck_results)
        percentage = random.randint(60, 99)
        
        embed = discord.Embed(
            title="🔮 اختبار الحظ",
            description=f"{result}\n\nنسبة الحظ: {percentage}%",
            color=0xe91e63
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='دعاء', aliases=['أدعية'])
    async def prayer(self, ctx):
        """مشاركة دعاء"""
        prayers = [
            "اللهم اهدنا فيمن هديت 🤲",
            "ربنا آتنا في الدنيا حسنة وفي الآخرة حسنة وقنا عذاب النار 🙏",
            "اللهم أعنا على ذكرك وشكرك وحسن عبادتك 💙",
            "ربنا اغفر لنا ذنوبنا وإسرافنا في أمرنا 🌟",
            "اللهم بارك لنا فيما رزقتنا ✨"
        ]
        
        prayer = random.choice(prayers)
        
        embed = discord.Embed(
            title="🤲 دعاء",
            description=prayer,
            color=0x27ae60
        )
        embed.set_footer(text="آمين يا رب العالمين")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='إحصائيات', aliases=['stats'])
    async def user_stats(self, ctx, member: discord.Member = None):
        """عرض إحصائيات المستخدم"""
        if not member:
            member = ctx.author
        
        # حساب بعض الإحصائيات البسيطة
        join_date = member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "غير معروف"
        account_age = (datetime.now() - member.created_at).days
        
        embed = discord.Embed(
            title=f"📊 إحصائيات {member.display_name}",
            color=member.color
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="📅 تاريخ الانضمام", value=join_date, inline=True)
        embed.add_field(name="🎂 عمر الحساب", value=f"{account_age} يوم", inline=True)
        embed.add_field(name="🏷️ الأدوار", value=len(member.roles)-1, inline=True)
        
        # إضافة بعض الإحصائيات المرحة
        activity_score = random.randint(1, 100)
        embed.add_field(name="⚡ نشاط الخادم", value=f"{activity_score}%", inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    """إعداد الإضافة"""
    await bot.add_cog(AdvancedCommands(bot))

