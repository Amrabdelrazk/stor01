import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from pathlib import Path

def create_excel_template():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "قالب_العهد"
    ws.sheet_view.rightToLeft = True

    headers = ["نوع الصنف", "اسم الصنف", "رقم السيريال", "الموظف"]
    ws.append(headers)

    header_fill = PatternFill("solid", fgColor="1E3A8A")
    header_font = Font(color="FFFFFF", bold=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    sample_data = [
        ["برنتر", "HP 1018", "CNC9149959", "احمد علي"],
        ["برنتر", "HP 1018", "CNC9149957", "مخزن"],
        ["كيس كمبيوتر", "DELL 3080", "856J9J3", "هند محمد"],
        ["فلاشة واي فاي", "D-LINK", "بدون", "احمد السعيد"]
    ]
    
    for row in sample_data:
        ws.append(row)

    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 30

    file_path = Path(__file__).resolve().parent / "قالب_استيراد_العهد.xlsx"
    wb.save(file_path)
    print(f"✅ تم إنشاء القالب بنجاح في: {file_path}")

if __name__ == "__main__":
    create_excel_template()