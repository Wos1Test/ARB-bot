#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ملف اختبار البوت العربي
يتحقق من صحة الإعدادات والملفات المطلوبة
"""

import os
import json
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """التحقق من وجود ملف"""
    if os.path.exists(file_path):
        print(f"✅ {description}: موجود")
        return True
    else:
        print(f"❌ {description}: غير موجود")
        return False

def check_env_file():
    """التحقق من ملف البيئة"""
    if not check_file_exists('.env', 'ملف البيئة (.env)'):
        return False
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'DISCORD_TOKEN=' in content and 'YOUR_BOT_TOKEN_HERE' not in content:
                print("✅ توكن البوت: تم إعداده")
                return True
            else:
                print("⚠️ توكن البوت: لم يتم إعداده بعد")
                return False
    except Exception as e:
        print(f"❌ خطأ في قراءة ملف .env: {e}")
        return False

def check_python_modules():
    """التحقق من المكتبات المطلوبة"""
    required_modules = ['discord', 'dotenv']
    all_good = True
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ مكتبة {module}: مثبتة")
        except ImportError:
            print(f"❌ مكتبة {module}: غير مثبتة")
            all_good = False
    
    return all_good

def check_bot_files():
    """التحقق من ملفات البوت"""
    required_files = [
        ('bot.py', 'الملف الرئيسي للبوت'),
        ('responses.py', 'ملف الردود العربية'),
        ('advanced_commands.py', 'ملف الأوامر المتقدمة'),
        ('channel_manager.py', 'مدير القنوات'),
        ('requirements.txt', 'قائمة المكتبات المطلوبة')
    ]
    
    all_good = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    return all_good

def test_json_files():
    """اختبار ملفات JSON (إنشاؤها إذا لم تكن موجودة)"""
    json_files = ['active_channels.json', 'channel_settings.json']
    
    for json_file in json_files:
        if not os.path.exists(json_file):
            try:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
                print(f"✅ {json_file}: تم إنشاؤه")
            except Exception as e:
                print(f"❌ خطأ في إنشاء {json_file}: {e}")
                return False
        else:
            print(f"✅ {json_file}: موجود")
    
    return True

def test_bot_syntax():
    """اختبار صحة كود البوت"""
    try:
        import ast
        with open('bot.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        ast.parse(code)
        print("✅ كود البوت: صحيح نحوياً")
        return True
    except SyntaxError as e:
        print(f"❌ خطأ نحوي في كود البوت: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ في فحص كود البوت: {e}")
        return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("🧪 بدء اختبار البوت العربي التفاعلي")
    print("=" * 50)
    
    tests = [
        ("فحص ملفات البوت", check_bot_files),
        ("فحص المكتبات المطلوبة", check_python_modules),
        ("فحص ملف البيئة", check_env_file),
        ("فحص ملفات JSON", test_json_files),
        ("فحص صحة الكود", test_bot_syntax)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"⚠️ فشل في: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"📊 نتائج الاختبار: {passed}/{total} نجح")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! البوت جاهز للتشغيل")
        print("\n🚀 لتشغيل البوت:")
        print("python bot.py")
    else:
        print("❌ بعض الاختبارات فشلت. يرجى إصلاح المشاكل قبل التشغيل")
        print("\n📋 قائمة المراجعة:")
        print("1. تأكد من تثبيت جميع المكتبات: pip install -r requirements.txt")
        print("2. أضف توكن البوت في ملف .env")
        print("3. تأكد من وجود جميع ملفات البوت")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

