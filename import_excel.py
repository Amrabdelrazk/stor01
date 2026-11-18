import sys
from pathlib import Path
from datetime import date
import openpyxl
import time
import random

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.database import SessionLocal, initialize_database
from models import Item, Employee, Category, Document, Transaction, Warehouse

EXCEL_FILE = BASE_DIR / "30-6-2026.xlsx"

def clean_text(val):
    if val is None: return ""
    return str(val).strip()

def generate_emp_code():
    return f"EMP-{int(time.time() * 1000) % 1000000:06d}-{random.randint(10, 99)}"

def run_import():
    if not EXCEL_FILE.exists():
        print(f"❌ لم يتم العثور على الملف: {EXCEL_FILE}")
        return

    print("⏳ جاري قراءة ملف الإكسيل...")
    wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
    sheet = wb.active

    initialize_database()
    session = SessionLocal()

    # ✅ 1. البحث عن مخزن الحاسب الآلي (عهدة)
    # بنجيب أي مخزن نوعه "عهدة"
    target_warehouse = session.query(Warehouse).filter_by(store_type="عهدة").first()
    if not target_warehouse:
        print("❌ مش لاقي أي مخزن نوعه (عهدة). تأكد إنك ضفت المخزن في البرنامج الأول.")
        return
    
    print(f"✅ تم العثور على المخزن: {target_warehouse.name}")

    # 2. إنشاء إذن الإضافة (الوارد) وإذن الصرف (العهد) وربطهم بالمخزن
    doc_in = session.query(Document).filter_by(doc_number="EXCEL-IN-001").first()
    if not doc_in:
        doc_in = Document(
            doc_type="IN", 
            doc_number="EXCEL-IN-001", 
            doc_date=date.today(), 
            warehouse_id=target_warehouse.id, # ✅ ربط بالمخزن
            notes="استيراد من الإكسيل - إضافة"
        )
        session.add(doc_in)
        session.commit()

    doc_out = session.query(Document).filter_by(doc_number="EXCEL-OUT-001").first()
    if not doc_out:
        doc_out = Document(
            doc_type="OUT", 
            doc_number="EXCEL-OUT-001", 
            doc_date=date.today(), 
            warehouse_id=target_warehouse.id, # ✅ ربط بالمخزن
            notes="استيراد من الإكسيل - عهد"
        )
        session.add(doc_out)
        session.commit()

    employees_cache = {}
    success_count = 0
    skipped_count = 0

    for row_idx, row in enumerate(sheet.iter_rows(min_row=4, values_only=True), start=4):
        cat_name = clean_text(row[1])
        model_name = clean_text(row[3])
        serial = clean_text(row[4])
        emp_name = clean_text(row[5])

        if not cat_name or "SUBTOTAL" in cat_name:
            continue

        if emp_name in ["مخزن", "مرتجع", "نقل", "بنك", ""]:
            skipped_count += 1
            continue

        if not serial or serial in ["بدون", "NA", "N/A"]:
            serial = f"NO-SN-{row_idx}"

        # 1. الفئة
        category = session.query(Category).filter_by(name=cat_name).first()
        if not category:
            category = Category(name=cat_name, code=f"CAT-{cat_name[:3]}")
            session.add(category)
            session.flush()

        # 2. الصنف
        item = session.query(Item).filter_by(code=serial).first()
        if not item:
            item = Item(
                code=serial, 
                name=f"{cat_name} {model_name} - {serial}", # ضفنا السيريال في الاسم
                category_id=category.id, 
                unit="قطعة", 
                min_qty=0
            )
            session.add(item)
            session.flush()

            trx_in = Transaction(document_id=doc_in.id, item_id=item.id, quantity=1, price=0, notes="جرد أولي - إضافة")
            session.add(trx_in)

        # 3. الموظف
        if emp_name not in employees_cache:
            emp = session.query(Employee).filter_by(name=emp_name).first()
            if not emp:
                emp = Employee(name=emp_name, code=generate_emp_code())
                session.add(emp)
                session.flush()
            employees_cache[emp_name] = emp.id

        emp_id = employees_cache[emp_name]

        # 4. حركة الصرف
        existing_trx = session.query(Transaction).filter_by(document_id=doc_out.id, item_id=item.id).first()
        if not existing_trx:
            trx_out = Transaction(document_id=doc_out.id, item_id=item.id, quantity=1, price=0, notes="جرد أولي - صرف عهدة")
            session.add(trx_out)
            doc_out.employee_id = emp_id
            success_count += 1

        if success_count % 20 == 0 and success_count > 0:
            session.commit()
            print(f"⏳ تم معالجة {success_count} جهاز...")

    session.commit()
    session.close()
    print(f"🎉 اكتمل الاستيراد!")
    print(f"✅ تم تسجيل: {success_count} جهاز في العهد (تابعين لمخزن: {target_warehouse.name}).")
    print(f"⏭️ تم تخطي: {skipped_count} جهاز.")

if __name__ == "__main__":
    run_import()