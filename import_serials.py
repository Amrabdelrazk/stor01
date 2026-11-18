import sys
from pathlib import Path
from datetime import date
import openpyxl
import time
import random
import re

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.database import SessionLocal, initialize_database
from models import Item, Employee, Category, Document, Transaction, Warehouse

# ⚠️ اسم ملف الإكسيل بتاعك
EXCEL_FILE = BASE_DIR / "data.xlsx" 

def clean_text(val):
    if val is None: return ""
    return str(val).strip()

def generate_emp_code():
    return f"EMP-{int(time.time() * 1000) % 1000000:06d}-{random.randint(10, 99)}"

def run_import():
    if not EXCEL_FILE.exists():
        print(f"❌ لم يتم العثور على الملف: {EXCEL_FILE}")
        return

    print("⏳ جاري قراءة ملف الإكسيل بذكاء...")
    wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
    sheet = wb.active

    # البحث عن صف العناوين (الترويسة) ديناميكياً
    header_row_idx = 1
    col_map = {}
    
    for row_idx, row in enumerate(sheet.iter_rows(min_row=1, max_row=10, values_only=True), start=1):
        row_text = [clean_text(c) for c in row]
        if "نوع الصنف" in row_text and "اسم الصنف" in row_text:
            header_row_idx = row_idx
            for i, cell_val in enumerate(row_text):
                if "نوع" in cell_val: col_map["cat"] = i
                elif "اسم الصنف" in cell_val: col_map["name"] = i
                elif "سيريال" in cell_val: col_map["serial"] = i
                elif "موظف" in cell_val: col_map["emp"] = i
            break

    if not col_map:
        print("❌ لم يتم العثور على صف العناوين (نوع الصنف، اسم الصنف...). تأكد من القالب.")
        return

    initialize_database()
    session = SessionLocal()

    target_warehouse = session.query(Warehouse).filter_by(store_type="عهدة").first()
    if not target_warehouse:
        print("❌ مش لاقي أي مخزن نوعه (عهدة).")
        return

    doc_in = Document(doc_type="IN", doc_number="IMPORT-IN-SMART", doc_date=date.today(), warehouse_id=target_warehouse.id, notes="استيراد سيريالات")
    doc_out = Document(doc_type="OUT", doc_number="IMPORT-OUT-SMART", doc_date=date.today(), warehouse_id=target_warehouse.id, notes="استيراد عهد")
    session.add(doc_in); session.add(doc_out); session.commit()

    items_cache = {}
    employees_cache = {}
    success_count = 0
    
    for row_idx, row in enumerate(sheet.iter_rows(min_row=header_row_idx+1, values_only=True), start=header_row_idx+1):
        cat_name = clean_text(row[col_map["cat"]]) if col_map.get("cat") is not None else ""
        model_name = clean_text(row[col_map["name"]]) if col_map.get("name") is not None else ""
        serial = clean_text(row[col_map["serial"]]) if col_map.get("serial") is not None else ""
        emp_name = clean_text(row[col_map["emp"]]) if col_map.get("emp") is not None else ""

        # تخطي السطور الفاضية أو سطور SUBTOTAL
        if not cat_name or "SUBTOTAL" in cat_name or not model_name:
            continue

        if not serial or serial in ["بدون", "NA", "N/A"]:
            serial = f"NO-SN-{row_idx}"

        # توليد كود فريد للصنف
        item_code = f"{cat_name[:3]}-{model_name.replace(' ', '-')[:10]}"
        item_name = f"{cat_name} {model_name}"

        # ─── 1. تسجيل الصنف ───
        if item_code not in items_cache:
            item = session.query(Item).filter_by(code=item_code).first()
            if not item:
                category = session.query(Category).filter_by(name=cat_name).first()
                if not category:
                    category = Category(name=cat_name, code=f"CAT-{cat_name[:3]}")
                    session.add(category)
                    session.flush()

                item = Item(code=item_code, name=item_name, category_id=category.id, unit="قطعة", min_qty=0)
                session.add(item)
                session.flush()
            items_cache[item_code] = item.id

        item_id = items_cache[item_code]

        # ─── 2. تسجيل الإضافة ───
        existing_in = session.query(Transaction).filter_by(document_id=doc_in.id, item_id=item_id, notes=f"سيريال: {serial}").first()
        if not existing_in:
            trx_in = Transaction(document_id=doc_in.id, item_id=item_id, quantity=1, price=0, notes=f"سيريال: {serial}")
            session.add(trx_in)

        # ─── 3. تسجيل الصرف (العهدة) ───
        if emp_name and emp_name not in ["مخزن", "مرتجع", "نقل", ""]:
            if emp_name not in employees_cache:
                emp = session.query(Employee).filter_by(name=emp_name).first()
                if not emp:
                    emp = Employee(name=emp_name, code=generate_emp_code())
                    session.add(emp)
                    session.flush()
                employees_cache[emp_name] = emp.id

            emp_id = employees_cache[emp_name]

            existing_out = session.query(Transaction).filter_by(document_id=doc_out.id, item_id=item_id, notes=f"سيريال: {serial}").first()
            if not existing_out:
                trx_out = Transaction(document_id=doc_out.id, item_id=item_id, quantity=1, price=0, notes=f"سيريال: {serial}")
                session.add(trx_out)
                doc_out.employee_id = emp_id
                success_count += 1

        if success_count % 20 == 0 and success_count > 0:
            session.commit()

    session.commit()
    session.close()
    print(f"🎉 اكتمل الاستيراد الذكي!")
    print(f"✅ تم تسجيل {success_count} جهاز في العهد.")

if __name__ == "__main__":
    run_import()