import os
import pyodbc

def get_database_config():
    """الحصول على إعدادات قاعدة البيانات المناسبة للبيئة"""
    
    # إعدادات Render
    if os.getenv('RENDER'):
        return {
            'server': os.getenv('DB_SERVER', ''),
            'database': os.getenv('DB_NAME', ''),
            'username': os.getenv('DB_USERNAME', ''),
            'password': os.getenv('DB_PASSWORD', ''),
            'driver': 'ODBC Driver 18 for SQL Server',
            'environment': 'render'
        }
    else:
        # إعدادات التطوير المحلي
        return {
            'server': 'localhost',
            'database': 'YourDatabaseName',
            'username': '',
            'password': '',
            'driver': 'SQL Server',
            'environment': 'local'
        }

def create_connection_string():
    """إنشاء سلسلة الاتصال بقاعدة البيانات"""
    config = get_database_config()
    
    if config['environment'] == 'render':
        if config['username'] and config['password']:
            # استخدام المصادقة باسم المستخدم وكلمة المرور
            connection_string = (
                f"DRIVER={{{config['driver']}}};"
                f"SERVER={config['server']};"
                f"DATABASE={config['database']};"
                f"UID={config['username']};"
                f"PWD={config['password']};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
                f"Connection Timeout=30;"
            )
        else:
            # استخدام Trusted Connection (للتطوير المحلي فقط)
            connection_string = (
                f"DRIVER={{{config['driver']}}};"
                f"SERVER={config['server']};"
                f"DATABASE={config['database']};"
                f"Trusted_Connection=yes;"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
            )
    else:
        # للإعدادات المحلية
        connection_string = (
            f"DRIVER={{{config['driver']}}};"
            f"SERVER={config['server']};"
            f"DATABASE={config['database']};"
            f"Trusted_Connection=yes;"
        )
    
    return connection_string

# المتغيرات العالمية
DB_CONFIG = get_database_config()
CONNECTION_STRING = create_connection_string()
SERVER = DB_CONFIG['server']
DATABASE = DB_CONFIG['database']

# اختبار الاتصال
def test_connection():
    """اختبار اتصال قاعدة البيانات"""
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ اتصال قاعدة البيانات ناجح")
        return True
    except Exception as e:
        print(f"❌ فشل اتصال قاعدة البيانات: {e}")
        return False

if __name__ == '__main__':
    test_connection()
