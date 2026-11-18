# build_license.spec
from pathlib import Path

BASE_DIR = Path(SPECPATH).resolve()

hiddenimports = [
    "utils.hwid", "utils.theme", "utils.password",
    "winreg", "tkinter", "tkinter.ttk", "tkinter.font", "tkinter.messagebox",
]

a = Analysis(
    ["license_generator.py"],
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    excludes=["sqlalchemy", "reportlab", "openpyxl", "pandas", "numpy"],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="LicenseGenerator",
    debug=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="LicenseGenerator",
)