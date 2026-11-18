# main.py
from __future__ import annotations
import sys
import traceback
import tkinter as tk
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import APP_NAME
from core.database import initialize_database, dispose_engine
from utils.theme import apply_theme
from utils import hwid as hwid_util
from views.login_view import LoginView
from views.main_view import MainView

LICENSE_FILE = BASE_DIR / "data" / "license.key"

def check_license() -> bool:
    current_hwid = hwid_util.get_hwid()
    error_msg = ""
    if LICENSE_FILE.exists():
        saved_code = LICENSE_FILE.read_text(encoding="utf-8").strip()
        is_valid, msg = hwid_util.verify_license(current_hwid, saved_code)
        if is_valid: return True
        else: error_msg = msg

    from views.activation_view import run_activation_gui
    return run_activation_gui(error_msg)
def run() -> None:
    try:
        if not check_license():
            sys.exit(0)

        initialize_database()

        from models import User
        if not User.get_by_username("admin"):
            User.create("admin", "admin123", "مدير النظام", role="admin")

        # إنشاء النافذة الرئيسية (مخفية)
        root = tk.Tk()
        root.withdraw() 
        root.title(APP_NAME)
        root.state('zoomed') # تكبير الشاشة
        apply_theme(root)

        # ─── عرض شاشة الترحيب ───
        from views.splash_view import SplashScreen
        splash = SplashScreen(root, duration=3.0)
        
        # انتظار إغلاق السبلاش (بأمان)
        root.wait_window(splash)
        
        # إظهار النافذة الرئيسية
        root.deiconify()
        
        def on_login_success(user):
            for child in root.winfo_children():
                child.destroy()
            MainView(root)

        from views.login_view import LoginView
        LoginView(root, on_success=on_login_success)

        root.mainloop()
        
    except Exception:
        import traceback
        traceback.print_exc()
        input("اضغط Enter للإغلاق...")
    finally:
        dispose_engine()
if __name__ == "__main__": run()