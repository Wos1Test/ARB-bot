#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import json
import os
from datetime import datetime

class ChannelManager(commands.Cog):
    """مدير القنوات للبوت العربي"""
    
    def __init__(self, bot):
        self.bot = bot
        self.channels_file = 'active_channels.json'
        self.settings_file = 'channel_settings.json'
        self.active_channels = self.load_active_channels()
        self.channel_settings = self.load_channel_settings()
    
    def load_active_channels(self):
        """تحميل قائمة القنوات النشطة"""
        try:
            with open(self.channels_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_active_channels(self):
        """حفظ قائمة القنوات النشطة"""
        with open(self.channels_file, 'w', encoding='utf-8') as f:
            json.dump(self.active_channels, f, ensure_ascii=False, indent=2)
    
    def load_channel_settings(self):
        """تحميل إعدادات القنوات"""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_channel_settings(self):
        """حفظ إعدادات القنوات"""
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.channel_settings, f, ensure_ascii=False, indent=2)
    
    def is_channel_active(self, guild_id, channel_id):
        """التحقق من نشاط القناة"""
        guild_str = str(guild_id)
        channel_str = str(channel_id)
        
        # إذا لم يتم تحديد قنوات للخادم، فجميع القنوات نشطة
        if guild_str not in self.active_channels:
            return True
        
        # إذا كانت القائمة فارغة، فجميع القنوات نشطة
        if not self.active_channels[guild_str]:
            return True
        
        return channel_str in self.active_channels[guild_str]
    
    def get_channel_settings(self, guild_id, channel_id):
        """الحصول على إعدادات القناة"""
        guild_str = str(guild_id)
        channel_str = str(channel_id)
        
        if guild_str in self.channel_settings and channel_str in self.channel_settings[guild_str]:
            return self.channel_settings[guild_str][channel_str]
        
        # الإعدادات الافتراضية
        return {
            'auto_react': True,
            'response_chance': 30,  # نسبة الرد التلقائي
            'welcome_messages': True,
            'time_greetings': True,
            'games_enabled': True
        }
    
    @commands.group(name='قناة', aliases=['channel'], invoke_without_command=True)
    async def channel_group(self, ctx):
        """مجموعة أوامر إدارة القنوات"""
        embed = discord.Embed(
            title="📺 إدارة القنوات",
            description="أوامر إدارة القنوات والتحكم في التفاعل",
            color=0x3498db
        )
        
        embed.add_field(
            name="🔧 الأوامر المتاحة",
            value="""
            `!قناة تفعيل` - تفعيل التفاعل في هذه القناة
            `!قناة إلغاء` - إلغاء التفاعل في هذه القناة
            `!قناة قائمة` - عرض القنوات النشطة
            `!قناة إعدادات` - عرض إعدادات القناة
            `!قناة تخصيص` - تخصيص إعدادات القناة
            `!قناة مسح` - مسح جميع الإعدادات
            """,
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @channel_group.command(name='تفعيل', aliases=['activate', 'enable'])
    @commands.has_permissions(manage_channels=True)
    async def activate_channel(self, ctx):
        """تفعيل التفاعل في القناة الحالية"""
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        
        if guild_id not in self.active_channels:
            self.active_channels[guild_id] = []
        
        if channel_id not in self.active_channels[guild_id]:
            self.active_channels[guild_id].append(channel_id)
            self.save_active_channels()
            
            embed = discord.Embed(
                title="✅ تم التفعيل",
                description=f"تم تفعيل التفاعل في قناة {ctx.channel.mention}",
                color=0x2ecc71
            )
            embed.add_field(
                name="📊 الإحصائيات",
                value=f"القنوات النشطة: {len(self.active_channels[guild_id])}",
                inline=True
            )
        else:
            embed = discord.Embed(
                title="ℹ️ معلومة",
                description=f"القناة {ctx.channel.mention} مفعلة مسبقاً",
                color=0x3498db
            )
        
        await ctx.send(embed=embed)
    
    @channel_group.command(name='إلغاء', aliases=['deactivate', 'disable'])
    @commands.has_permissions(manage_channels=True)
    async def deactivate_channel(self, ctx):
        """إلغاء التفاعل في القناة الحالية"""
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        
        if guild_id in self.active_channels and channel_id in self.active_channels[guild_id]:
            self.active_channels[guild_id].remove(channel_id)
            self.save_active_channels()
            
            embed = discord.Embed(
                title="❌ تم الإلغاء",
                description=f"تم إلغاء التفاعل في قناة {ctx.channel.mention}",
                color=0xe74c3c
            )
        else:
            embed = discord.Embed(
                title="ℹ️ معلومة",
                description=f"القناة {ctx.channel.mention} غير مفعلة",
                color=0x3498db
            )
        
        await ctx.send(embed=embed)
    
    @channel_group.command(name='قائمة', aliases=['list', 'show'])
    async def list_channels(self, ctx):
        """عرض قائمة القنوات النشطة"""
        guild_id = str(ctx.guild.id)
        
        embed = discord.Embed(
            title="📺 القنوات النشطة",
            color=0x9b59b6
        )
        
        if guild_id not in self.active_channels or not self.active_channels[guild_id]:
            embed.description = "🌐 جميع القنوات نشطة (لم يتم تحديد قنوات محددة)"
            embed.add_field(
                name="💡 نصيحة",
                value="استخدم `!قناة تفعيل` لتحديد قنوات محددة للتفاعل",
                inline=False
            )
        else:
            channels_list = []
            for channel_id in self.active_channels[guild_id]:
                channel = self.bot.get_channel(int(channel_id))
                if channel:
                    settings = self.get_channel_settings(ctx.guild.id, channel_id)
                    status = "🟢" if settings['auto_react'] else "🟡"
                    channels_list.append(f"{status} {channel.mention}")
            
            if channels_list:
                embed.description = "\n".join(channels_list)
                embed.add_field(
                    name="📊 الإحصائيات",
                    value=f"إجمالي القنوات: {len(channels_list)}",
                    inline=True
                )
            else:
                embed.description = "❌ لا توجد قنوات صالحة"
        
        embed.set_footer(text="🟢 نشط كاملاً | 🟡 نشط جزئياً")
        await ctx.send(embed=embed)
    
    @channel_group.command(name='إعدادات', aliases=['settings', 'config'])
    async def channel_settings(self, ctx):
        """عرض إعدادات القناة الحالية"""
        settings = self.get_channel_settings(ctx.guild.id, ctx.channel.id)
        
        embed = discord.Embed(
            title=f"⚙️ إعدادات {ctx.channel.name}",
            color=0xf39c12
        )
        
        embed.add_field(
            name="🤖 التفاعل التلقائي",
            value="✅ مفعل" if settings['auto_react'] else "❌ معطل",
            inline=True
        )
        
        embed.add_field(
            name="🎲 نسبة الرد",
            value=f"{settings['response_chance']}%",
            inline=True
        )
        
        embed.add_field(
            name="👋 رسائل الترحيب",
            value="✅ مفعل" if settings['welcome_messages'] else "❌ معطل",
            inline=True
        )
        
        embed.add_field(
            name="🕐 تحيات الوقت",
            value="✅ مفعل" if settings['time_greetings'] else "❌ معطل",
            inline=True
        )
        
        embed.add_field(
            name="🎮 الألعاب",
            value="✅ مفعل" if settings['games_enabled'] else "❌ معطل",
            inline=True
        )
        
        embed.set_footer(text="استخدم !قناة تخصيص لتعديل الإعدادات")
        
        await ctx.send(embed=embed)
    
    @channel_group.command(name='تخصيص', aliases=['customize', 'set'])
    @commands.has_permissions(manage_channels=True)
    async def customize_channel(self, ctx, setting=None, value=None):
        """تخصيص إعدادات القناة"""
        if not setting:
            embed = discord.Embed(
                title="⚙️ الإعدادات المتاحة",
                description="استخدم: `!قناة تخصيص <الإعداد> <القيمة>`",
                color=0xf39c12
            )
            
            embed.add_field(
                name="📝 الإعدادات",
                value="""
                `auto_react` - التفاعل التلقائي (true/false)
                `response_chance` - نسبة الرد (1-100)
                `welcome_messages` - رسائل الترحيب (true/false)
                `time_greetings` - تحيات الوقت (true/false)
                `games_enabled` - الألعاب (true/false)
                """,
                inline=False
            )
            
            await ctx.send(embed=embed)
            return
        
        guild_str = str(ctx.guild.id)
        channel_str = str(ctx.channel.id)
        
        # إنشاء الإعدادات إذا لم تكن موجودة
        if guild_str not in self.channel_settings:
            self.channel_settings[guild_str] = {}
        if channel_str not in self.channel_settings[guild_str]:
            self.channel_settings[guild_str][channel_str] = self.get_channel_settings(ctx.guild.id, ctx.channel.id)
        
        settings = self.channel_settings[guild_str][channel_str]
        
        # تحديث الإعداد
        if setting in ['auto_react', 'welcome_messages', 'time_greetings', 'games_enabled']:
            if value.lower() in ['true', '1', 'نعم', 'مفعل']:
                settings[setting] = True
                status = "✅ مفعل"
            elif value.lower() in ['false', '0', 'لا', 'معطل']:
                settings[setting] = False
                status = "❌ معطل"
            else:
                await ctx.send("❌ قيمة غير صحيحة. استخدم: true/false أو نعم/لا")
                return
        
        elif setting == 'response_chance':
            try:
                chance = int(value)
                if 1 <= chance <= 100:
                    settings[setting] = chance
                    status = f"{chance}%"
                else:
                    await ctx.send("❌ النسبة يجب أن تكون بين 1 و 100")
                    return
            except ValueError:
                await ctx.send("❌ يرجى إدخال رقم صحيح")
                return
        
        else:
            await ctx.send("❌ إعداد غير معروف")
            return
        
        # حفظ الإعدادات
        self.save_channel_settings()
        
        embed = discord.Embed(
            title="✅ تم التحديث",
            description=f"تم تحديث `{setting}` إلى: {status}",
            color=0x2ecc71
        )
        
        await ctx.send(embed=embed)
    
    @channel_group.command(name='مسح', aliases=['reset', 'clear'])
    @commands.has_permissions(administrator=True)
    async def reset_settings(self, ctx):
        """مسح جميع إعدادات الخادم"""
        guild_str = str(ctx.guild.id)
        
        # مسح القنوات النشطة
        if guild_str in self.active_channels:
            del self.active_channels[guild_str]
            self.save_active_channels()
        
        # مسح إعدادات القنوات
        if guild_str in self.channel_settings:
            del self.channel_settings[guild_str]
            self.save_channel_settings()
        
        embed = discord.Embed(
            title="🗑️ تم المسح",
            description="تم مسح جميع إعدادات القنوات والتفاعل في الخادم",
            color=0xe74c3c
        )
        embed.add_field(
            name="ℹ️ ملاحظة",
            value="سيعود البوت للتفاعل في جميع القنوات بالإعدادات الافتراضية",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    """إعداد الإضافة"""
    await bot.add_cog(ChannelManager(bot))

