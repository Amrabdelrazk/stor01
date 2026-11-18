from core.database import get_session
from models import Item, Category
from sqlalchemy import select, func

with get_session() as s:
    cats = s.scalars(select(Category)).all()
    print(f'--- إجمالي الفئات: {len(cats)} ---')
    for c in cats:
        print(f'ID: {c.id} | الاسم: {c.name}')
        
    print('\n--- إجمالي الأصناف ---')
    total_items = s.scalar(select(func.count(Item.id)))
    print(f'عدد الأصناف: {total_items}')
    
    items_with_cat = s.scalar(select(func.count(Item.id)).where(Item.category_id.isnot(None)))
    print(f'أصناف متسجللها فئة: {items_with_cat}')
    print(f'أصناف من غير فئة: {total_items - items_with_cat}')