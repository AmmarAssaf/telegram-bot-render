#!/usr/bin/env python3
# ==============================
# 🚀 تطبيق البوت لـ Render
# ==============================

import os
import logging
import asyncio
import threading
from flask import Flask
import time

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تطبيق Flask
app = Flask(__name__)

# متغير عالمي للتطبيق
application = None

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 بوت التليجرام</title>
        <meta charset="utf-8">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                max-width: 600px;
                margin: 0 auto;
            }
            .success { 
                color: #4CAF50; 
                font-size: 28px; 
                font-weight: bold;
                margin-bottom: 20px;
            }
            .info { 
                color: #E3F2FD; 
                margin: 15px 0; 
                font-size: 18px;
            }
            .footer {
                margin-top: 30px;
                font-size: 14px;
                color: #BBDEFB;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success">✅ البوت يعمل بنجاح على Render!</div>
            <div class="info">🤖 بوت مؤسسة الترويج الإعلامي</div>
            <div class="info">📞 للاستفسارات: /support في التليجرام</div>
            <div class="info">🕒 وقت التشغيل: {}</div>
            <div class="footer">
                تم النشر بنجاح على Render | 🤖 نظام البوت المتكامل
            </div>
        </div>
        <script>
            function updateTime() {
                const now = new Date();
                document.querySelector('.info:nth-child(4)').textContent = 
                    '🕒 وقت التشغيل: ' + now.toLocaleString('ar-SA');
            }
            setInterval(updateTime, 1000);
            updateTime();
        </script>
    </body>
    </html>
    """.format(time.strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/health')
def health():
    return {
        "status": "healthy", 
        "service": "telegram-bot",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "environment": "render"
    }

@app.route('/test')
def test():
    return "✅ البوت يعمل بشكل صحيح!"

def run_bot():
    """تشغيل البوت الرئيسي"""
    try:
        # استيراد وتشغيل البوت الرئيسي
        print("🔄 جاري تحميل البوت الرئيسي...")
        
        # استيراد الملف الرئيسي للبوت
        import sys
        import importlib.util
        
        # تحديد مسار الملف الرئيسي
        main_bot_file = "end_main_Copy"  # بدون .py
        
        try:
            # محاولة الاستيراد الديناميكي
            spec = importlib.util.spec_from_file_location("main_bot", "end main - Copy.py")
            main_bot_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_bot_module)
            
            # تشغيل البوت
            print("🚀 بدء تشغيل البوت على Render...")
            main_bot_module.main()
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البوت: {e}")
            # المحاولة بطريقة بديلة
            try:
                from end_main_Copy import main
                main()
            except Exception as e2:
                print(f"❌ خطأ بديل: {e2}")
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
        import traceback
        traceback.print_exc()

def run_flask():
    """تشغيل خادم Flask"""
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 بدء خادم Flask على المنفذ {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 بدء تشغيل تطبيق البوت على Render")
    print("=" * 50)
    
    # تشغيل البوت في خيط منفصل
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("✅ تم بدء خيط البوت بنجاح")
    print("🌐 جاري تشغيل خادم الويب...")
    
    # تشغيل Flask في الخيط الرئيسي
    run_flask()