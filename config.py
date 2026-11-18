# config.py
"""
الإعدادات العامة للنظام
Developer: AMR ABDELRAZK (AMRABDLRAZK2022@GMAIL.COM)
© 2026 - All Rights Reserved
"""
from pathlib import Path

# ─── المسارات الأساسية ────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "warehouse.db"
ATTACHMENTS_DIR = DATA_DIR / "attachments"
BACKUPS_DIR = DATA_DIR / "backups"

# إنشاء المجلدات إن لم تكن موجودة
for _p in (DATA_DIR, ATTACHMENTS_DIR, BACKUPS_DIR):
    _p.mkdir(parents=True, exist_ok=True)

# ─── إعدادات قاعدة البيانات ──────────────────────────
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"
SQL_ECHO = False           # اجعلها True لتتبع الاستعلامات أثناء التطوير
POOL_SIZE = 5
POOL_PRECONNECT = True

# ─── معلومات التطبيق ─────────────────────────────────
APP_NAME = "نظام إدارة المخازن"
APP_VERSION = "2.0.0-MVC"
DEVELOPER = "AMR ABDELRAZK"
DEVELOPER_EMAIL = "AMRABDLRAZK2022@GMAIL.COM"
COPYRIGHT = "© 2026 AMR ABDELRAZK - All Rights Reserved"

# ─── الثوابت التجارية ────────────────────────────────
TRANSACTION_TYPES = {
    "IN":  "إضافة",
    "OUT": "صرف",
    "RET": "إرجاع",
    "DIS": "استبعاد",
}

USER_ROLES = {
    "admin":  "مدير النظام",
    "editor": "محرر",
    "viewer": "مشاهد",
    "custom": "مخصص",
}

# ─── إعدادات الأمان ──────────────────────────────────
HWID_REQUIRED = True       # تفعيل فحص الهارد وير
SESSION_TIMEOUT_MIN = 60   # انتهاء الجلسة بعد دقيقة خمول
PASSWORD_MIN_LENGTH = 6