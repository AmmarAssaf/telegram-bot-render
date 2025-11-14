from flask import Flask
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    """صفحة الرئيسية لتأكيد أن البوت يعمل"""
    try:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bot Status</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 10px;
                    backdrop-filter: blur(10px);
                }
                .status { 
                    color: #4CAF50; 
                    font-weight: bold;
                    font-size: 1.2em;
                }
                .error {
                    color: #ff4444;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Bot Status</h1>
                <p>Bot is running successfully on Render</p>
                <p>Last updated: {}</p>
                <p class="status">Status: ✅ Active and Running</p>
                <p>Environment: {}</p>
                <hr>
                <p><strong>Features:</strong></p>
                <ul>
                    <li>✅ Telegram Bot Integration</li>
                    <li>✅ Database Connection</li>
                    <li>✅ Automatic Backup Systems</li>
                    <li>✅ User Registration System</li>
                </ul>
            </div>
        </body>
        </html>
        """.format(
            time.strftime("%Y-%m-%d %H:%M:%S"),
            os.getenv('RENDER', 'Development')
        )
        return html_content
    except Exception as e:
        return f"""
        <html>
        <body>
            <h1>Bot Status</h1>
            <p class="error">Error in template: {str(e)}</p>
            <p>Time: {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
        </body>
        </html>
        """

@app.route('/health')
def health():
    """نقطة فحص الصحة للـ health checks"""
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
