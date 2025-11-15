from flask import Flask
import time
import os
import threading

app = Flask(__name__)

# محاولة استيراد البوت الرئيسي
try:
    from main import main as bot_main
    BOT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ تحذير: لا يمكن تحميل البوت الرئيسي: {e}")
    BOT_AVAILABLE = False
except Exception as e:
    print(f"⚠️ تحذير: خطأ في تحميل البوت: {e}")
    BOT_AVAILABLE = False

def run_bot():
    """تشغيل البوت في خيط منفصل"""
    if BOT_AVAILABLE:
        try:
            print("🤖 بدء تشغيل البوت في خيط منفصل...")
            bot_main()
        except Exception as e:
            print(f"❌ خطأ في تشغيل البوت: {e}")

@app.route('/')
def home():
    """الصفحة الرئيسية"""
    try:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        environment = os.getenv('RENDER', 'Development')
        
        status = "✅ Active and Running" if BOT_AVAILABLE else "❌ Bot Not Available"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bot Status</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 10px;
                    backdrop-filter: blur(10px);
                }}
                .status {{ 
                    color: #4CAF50; 
                    font-weight: bold;
                    font-size: 1.2em;
                }}
                .error {{
                    color: #ff4444;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Bot Status</h1>
                <p>Telegram Bot Service</p>
                <p>Last updated: {current_time}</p>
                <p class="status">Status: {status}</p>
                <p>Environment: {environment}</p>
                <hr>
                <p><strong>Features:</strong></p>
                <ul>
                    <li>✅ Telegram Bot Integration</li>
                    <li>✅ User Registration System</li>
                    <li>✅ Database Management</li>
                    <li>✅ Automatic Backups</li>
                </ul>
            </div>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"<h1>Bot Status</h1><p>Error: {str(e)}</p>"

@app.route('/health')
def health():
    """نقطة فحص الصحة"""
    return {"status": "healthy", "timestamp": time.time(), "bot_available": BOT_AVAILABLE}

if __name__ == '__main__':
    # بدء البوت في خيط منفصل
    if BOT_AVAILABLE:
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        print("✅ تم بدء خيط البوت بنجاح")
    
    # تشغيل خادم الويب
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 بدء خادم Flask على المنفذ {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
