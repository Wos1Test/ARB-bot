#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import datetime

class ArabicResponses:
    """فئة للردود العربية المتقدمة"""
    
    # ردود حسب الوقت
    TIME_RESPONSES = {
        'morning': [
            'صباح الخير والنشاط! ☀️',
            'صباح مليء بالإنجازات! 🌅',
            'أسعد الله صباحك بكل خير! 🌸',
            'صباح البركة والتوفيق! ✨'
        ],
        'afternoon': [
            'ظهيرة مباركة! ☀️',
            'نهارك سعيد! 😊',
            'أوقات مثمرة! 💪',
            'استمر في التميز! 🌟'
        ],
        'evening': [
            'مساء الخير والراحة! 🌙',
            'مساء هادئ ومريح! 🌆',
            'أسعد الله مساءك! ⭐',
            'مساء مليء بالسكينة! 🌺'
        ],
        'night': [
            'ليلة سعيدة! 🌙',
            'أحلام جميلة! ✨',
            'راحة مستحقة! 😴',
            'ليلة مباركة! 🌟'
        ]
    }
    
    # ردود تفاعلية متنوعة
    INTERACTIVE_RESPONSES = {
        'compliments': [
            'أنت شخص رائع! 🌟',
            'تستحق كل التقدير! 👏',
            'مبدع كما عهدناك! ✨',
            'واصل هذا التميز! 💪'
        ],
        'motivation': [
            'لا تستسلم أبداً! 💪',
            'أنت أقوى مما تتخيل! 🦁',
            'النجاح ينتظرك! 🎯',
            'كل خطوة تقربك من الهدف! 🚀'
        ],
        'wisdom': [
            'الصبر مفتاح الفرج 🗝️',
            'العلم نور والجهل ظلام 💡',
            'من جد وجد ومن زرع حصد 🌱',
            'الطريق إلى النجاح يبدأ بخطوة واحدة 👣'
        ],
        'fun': [
            'الضحك يطيل العمر! 😄',
            'ابتسامتك تضيء اليوم! 😊',
            'المرح جزء من الحياة! 🎉',
            'السعادة معدية، انشرها! 😁'
        ]
    }
    
    # ردود على المشاعر
    EMOTION_RESPONSES = {
        'happy': [
            'أراك سعيداً اليوم! 😊',
            'السعادة تشع منك! ✨',
            'فرحتك تسعدني! 🎉',
            'استمر في هذا المزاج الرائع! 😄'
        ],
        'sad': [
            'أتمنى أن تشعر بتحسن قريباً 💙',
            'الأيام الصعبة تمر، والأجمل قادم 🌈',
            'أنا هنا إذا احتجت للحديث 🤗',
            'كل شيء سيكون بخير بإذن الله 🙏'
        ],
        'excited': [
            'أشاركك الحماس! 🎉',
            'طاقتك الإيجابية رائعة! ⚡',
            'هذا الحماس معدي! 🔥',
            'واصل هذه الروح المتفائلة! 🚀'
        ],
        'tired': [
            'خذ قسطاً من الراحة 😴',
            'الراحة حق مشروع 🛋️',
            'أنت تستحق الاستراحة 💤',
            'اعتن بنفسك أولاً 💙'
        ]
    }
    
    # أسئلة تفاعلية
    QUESTIONS = [
        'كيف كان يومك؟ 🤔',
        'ما هو أفضل شيء حدث لك اليوم؟ ✨',
        'هل تعلمت شيئاً جديداً اليوم؟ 📚',
        'ما هي خططك للغد؟ 📅',
        'ما هو هدفك الحالي؟ 🎯'
    ]
    
    @staticmethod
    def get_time_based_response():
        """الحصول على رد حسب الوقت الحالي"""
        now = datetime.datetime.now()
        hour = now.hour
        
        if 5 <= hour < 12:
            return random.choice(ArabicResponses.TIME_RESPONSES['morning'])
        elif 12 <= hour < 17:
            return random.choice(ArabicResponses.TIME_RESPONSES['afternoon'])
        elif 17 <= hour < 22:
            return random.choice(ArabicResponses.TIME_RESPONSES['evening'])
        else:
            return random.choice(ArabicResponses.TIME_RESPONSES['night'])
    
    @staticmethod
    def get_random_response(category):
        """الحصول على رد عشوائي من فئة معينة"""
        if category in ArabicResponses.INTERACTIVE_RESPONSES:
            return random.choice(ArabicResponses.INTERACTIVE_RESPONSES[category])
        return "أهلاً بك! 😊"
    
    @staticmethod
    def get_emotion_response(emotion):
        """الحصول على رد حسب المشاعر"""
        if emotion in ArabicResponses.EMOTION_RESPONSES:
            return random.choice(ArabicResponses.EMOTION_RESPONSES[emotion])
        return "أفهم مشاعرك 💙"
    
    @staticmethod
    def get_random_question():
        """الحصول على سؤال عشوائي للتفاعل"""
        return random.choice(ArabicResponses.QUESTIONS)

# إيموجي عربية شائعة
ARABIC_EMOJIS = {
    'celebration': ['🎉', '🎊', '✨', '🌟', '💫', '🎈'],
    'love': ['❤️', '💙', '💚', '💛', '💜', '🧡', '💖'],
    'nature': ['🌸', '🌺', '🌻', '🌹', '🌷', '🌿', '🍃'],
    'success': ['👏', '💪', '🏆', '🥇', '🎯', '🚀', '⭐'],
    'peace': ['☮️', '🕊️', '🤲', '🙏', '💙', '🌈'],
    'wisdom': ['📚', '💡', '🧠', '🔍', '📖', '✍️'],
    'time': ['⏰', '🕐', '⌚', '📅', '🗓️', '⏳'],
    'weather': ['☀️', '🌙', '⭐', '🌅', '🌆', '🌈', '☁️']
}

def get_random_emoji(category='celebration'):
    """الحصول على إيموجي عشوائي من فئة معينة"""
    if category in ARABIC_EMOJIS:
        return random.choice(ARABIC_EMOJIS[category])
    return '😊'

