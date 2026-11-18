# license_generator.py
"""
أداة توليد أكواد الترخيص (للمطور فقط)
- لا تُعطى للعميل.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import hashlib
from utils.theme import Colors, Fonts

SECRET = "AMRABDLRAZK2026"

# ─── دوال التوليد (متوافقة مع verify_license في utils/hwid.py) ───
def generate_license_key(hwid: str, expiry_date_str: str) -> str:
    # توليد الهاش (16 حرف)
    raw = f"{hwid}|{expiry_date_str}|{SECRET}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest().upper()[:16]
    code = "-".join(digest[i:i+4] for i in range(0, 16, 4))
    
    # إضافة التاريخ (YYMMDD) كجزء خامس
    date_part = expiry_date_str.replace("-", "")[2:] 
    return f"{code}-{date_part}"

class LicenseGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔑 أداة توليد التراخيص (للمطور)")
        self.geometry("550x550")
        self.configure(bg=Colors.BG)
        self.resizable(False, False)
        
        # توسيط الشاشة
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"+{x}+{y}")
        
        self._build()

    def _build(self):
        tk.Label(self, text="مولد أكواد التفعيل", bg=Colors.BG, fg=Colors.TEXT, font=Fonts.get(Fonts.SIZE_XXL, bold=True)).pack(pady=(20, 5))
        tk.Label(self, text="هذه الأداة خاصة بالمطور فقط.", bg=Colors.BG, fg=Colors.TEXT_DIM, font=Fonts.get(Fonts.SIZE_MD)).pack(pady=(0, 20))

        card = tk.Frame(self, bg=Colors.BG_ALT, padx=30, pady=20, highlightthickness=1, highlightbackground=Colors.BORDER_HI)
        card.pack(padx=30, fill="both", expand=True)

        # 1. بصمة الجهاز (HWID)
        tk.Label(card, text="1. بصمة جهاز العميل (HWID):", bg=Colors.BG_ALT, fg=Colors.TEXT, font=Fonts.get(Fonts.SIZE_MD, bold=True)).pack(anchor="e")
        
        req_frame = tk.Frame(card, bg=Colors.BG_ALT); req_frame.pack(fill="x", pady=(0, 15))
        self.hwid_var = tk.StringVar()
        ttk.Entry(req_frame, textvariable=self.hwid_var, font=Fonts.get(Fonts.SIZE_MD), justify="center").pack(side="right", fill="x", expand=True, ipady=4)
        
        ttk.Button(req_frame, text="عشوائي (للتجربة)", width=14, command=self._random_hwid).pack(side="left", padx=(10, 0))

        # 2. تاريخ الانتهاء
        tk.Label(card, text="2. تاريخ انتهاء الترخيص:", bg=Colors.BG_ALT, fg=Colors.TEXT, font=Fonts.get(Fonts.SIZE_MD, bold=True)).pack(anchor="e", pady=(10, 4))
        
        self.date_var = tk.StringVar(value=(date.today() + timedelta(days=365)).isoformat())
        ttk.Entry(card, textvariable=self.date_var, font=Fonts.get(Fonts.SIZE_LG), justify="center").pack(fill="x", pady=(0, 10), ipady=4)

        # أزرار سريعة للتاريخ
        btn_frame = tk.Frame(card, bg=Colors.BG_ALT); btn_frame.pack(fill="x", pady=(0, 20))
        for text, days in [("شهر",30), ("6 أشهر",180), ("سنة",365), ("سنتان",730)]:
            ttk.Button(btn_frame, text=text, command=lambda d=days: self.date_var.set((date.today() + timedelta(days=d)).isoformat())).pack(side="right", padx=2, expand=True)

        # 3. الكود الناتج
        tk.Label(card, text="3. كود التفعيل الناتج:", bg=Colors.BG_ALT, fg=Colors.TEXT, font=Fonts.get(Fonts.SIZE_MD, bold=True)).pack(anchor="e")
        
        self.result_var = tk.StringVar()
        res_entry = ttk.Entry(card, textvariable=self.result_var, font=Fonts.get(Fonts.SIZE_LG, bold=True), justify="center", state="readonly")
        res_entry.pack(fill="x", pady=(0, 10), ipady=6)

        ttk.Button(card, text="⚙️ توليد الكود", style="Primary.TButton", command=self._generate).pack(fill="x", ipady=3)
        ttk.Button(card, text="📋 نسخ الكود", style="Success.TButton", command=self._copy).pack(fill="x", ipady=3, pady=(5, 0))

    def _random_hwid(self):
        import random, string
        fake = ''.join(random.choices(string.hexdigits.lower(), k=32))
        self.hwid_var.set(fake)

    def _generate(self):
        hwid = self.hwid_var.get().strip()
        expiry = self.date_var.get().strip()
        
        if not hwid or len(hwid) != 32:
            return messagebox.showerror("خطأ", "بصمة الجهاز (HWID) يجب أن تكون 32 حرفاً.", parent=self)
        if not expiry:
            return messagebox.showerror("خطأ", "يرجى إدخال تاريخ الانتهاء.", parent=self)
        
        try:
            code = generate_license_key(hwid, expiry)
            self.result_var.set(code)
        except Exception as e:
            messagebox.showerror("خطأ", str(e), parent=self)

    def _copy(self):
        code = self.result_var.get()
        if not code:
            return messagebox.showinfo("تنبيه", "قم بتوليد الكود أولاً.", parent=self)
        self.clipboard_clear()
        self.clipboard_append(code)
        messagebox.showinfo("تم النسخ", "تم نسخ الكود إلى الحافظة.", parent=self)

if __name__ == "__main__":
    app = LicenseGeneratorApp()
    app.mainloop()