# build.spec
from pathlib import Path

BASE_DIR = Path(SPECPATH).resolve()

datas = [
    (str(BASE_DIR / "config.py"), "."),
    # إذا كان لديك ملفات خطوط (ttf) أضفها هنا
    # (str(BASE_DIR / "assets" / "arial.ttf"), "assets"),
]

hiddenimports = [
    "sqlalchemy", "sqlalchemy.dialects.sqlite", "sqlalchemy.orm", "sqlite3",
    "openpyxl", "openpyxl.styles", "openpyxl.utils",
    "reportlab", "reportlab.pdfgen", "reportlab.pdfbase", "reportlab.pdfbase.ttfonts", "reportlab.platypus",
    "arabic_reshaper", "bidi", "bidi.algorithm",
    "winreg", "tkinter", "tkinter.ttk", "tkinter.font", "tkinter.filedialog", "tkinter.messagebox",
    "core", "core.database", "core.base_model", "core.exceptions",
    "models", "controllers", "views", "utils",
    "utils.theme", "utils.hwid", "utils.password", "utils.validators", 
    "utils.ui_helpers", "utils.excel_io", "utils.pdf_gen",
]

a = Analysis(
    ["main.py"],
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "numpy", "scipy", "pandas", "PyQt5", "PySide2", "IPython", "pytest"],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="WarehouseSystem",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # ← False تعني عدم ظهور شاشة سوداء
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # ← إذا كان لديك أيقونة، ضع مسارها هنا
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="WarehouseSystem",
)