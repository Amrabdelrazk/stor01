import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.database import get_session
from models import Category, Item, Transaction, Document
from sqlalchemy import select, func, case

print("⏳ جاري فحص قاعدة البيانات...")

with get_session() as s:
    # 1. نجيب كل الفئات
    categories = s.scalars(select(Category).order_by(Category.name)).all()
    print(f"\n✅ عدد الفئات في قاعدة البيانات: {len(categories)}")
    
    if len(categories) == 0:
        print("❌ المشكلة: مفيش فئات في قاعدة البيانات أصلاً!")
    else:
        # 2. نجرب نجيب بيانات أول 3 فئات فقط للتجربة
        print("\n⏳ جاري حساب أرصدة الفئات...")
        for cat in categories[:3]:
            signed = case((Document.doc_type.in_(["IN", "RET"]), Transaction.quantity), else_=-Transaction.quantity)
            
            bal_query = (
                select(func.coalesce(func.sum(signed), 0))
                .select_from(Transaction)
                .join(Document, Document.id == Transaction.document_id)
                .join(Item, Item.id == Transaction.item_id)
                .where(Item.category_id == cat.id)
            )
            
            try:
                total_bal = float(s.scalar(bal_query) or 0)
                print(f"   - فئة [{cat.name}]: الرصيد = {total_bal}")
            except Exception as e:
                print(f"   - ❌ خطأ في حساب فئة [{cat.name}]: {e}")

print("\n✅ انتهى الفحص.")