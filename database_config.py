# database_config.py
import os
import urllib.parse

def get_database_config():
    """اكتشاف تلقائي للبيئة المحلية أو السحابية"""
    try:
        # إذا كان على Render (بيئة سحابية)
        if 'DATABASE_URL' in os.environ:
            database_url = os.environ['DATABASE_URL']
            
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)
            
            parsed_url = urllib.parse.urlparse(database_url)
            
            return {
                'driver': 'PostgreSQL',
                'server': parsed_url.hostname,
                'database': parsed_url.path[1:],
                'user': parsed_url.username,
                'password': parsed_url.password,
                'port': parsed_url.port or 5432,
                'environment': 'render'
            }
        else:
            # البيئة المحلية
            return {
                'driver': 'SQL Server',
                'server': r'DESKTOP-MO9M6P1\MSSQL',
                'database': 'TelegramBotDB',
                'trusted_connection': 'yes',
                'environment': 'local'
            }
    except Exception as e:
        print(f"❌ خطأ في إعداد قاعدة البيانات: {e}")
        return None

def create_connection_string(config):
    """إنشاء سلسلة اتصال مرنة"""
    if not config:
        return None
        
    if config['driver'] == 'SQL Server':
        return f'DRIVER={{SQL Server}};SERVER={config["server"]};DATABASE={config["database"]};Trusted_Connection=yes;'
    else:  # PostgreSQL
        return f"postgresql://{config['user']}:{config['password']}@{config['server']}:{config['port']}/{config['database']}"

# الحصول على إعدادات قاعدة البيانات
DB_CONFIG = get_database_config()
CONNECTION_STRING = create_connection_string(DB_CONFIG) if DB_CONFIG else None

# تعريف SERVER و DATABASE للتوافق مع الكود القديم
SERVER = DB_CONFIG['server'] if DB_CONFIG else r'DESKTOP-MO9M6P1\MSSQL'
DATABASE = DB_CONFIG['database'] if DB_CONFIG else 'TelegramBotDB'
