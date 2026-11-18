import sys
from pathlib import Path
from datetime import date
import re

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.database import SessionLocal, initialize_database
from models import Item, Employee, Category, Document, Transaction

# البيانات (نفس البيانات السابقة)
raw_data = """
كيس كمبيوتر	DELL 3080	856J9J3
كيس كمبيوتر	DELL 3080	FN7J9J3	هند محمد شفيق عبد الفتاح
كيس كمبيوتر	DELL 3080	G36J9H3	ايمان احمد عادل محمود عبد الحي
كيس كمبيوتر	DELL 3080	GW5J9J3	سندس عبد العزيز مصطفي
كيس كمبيوتر	DELL 3080	346J9J3	مرتجع
كيس كمبيوتر	DELL 5090	DL8P2N3	اشرف ابراهيم محمد احمد
كيس كمبيوتر	DELL 5090	26W21N3	سمية صلاح الدين اسماعيل خطاب
كيس كمبيوتر	DELL 5090	F6W21N3	اسلام سامي محمد فوزي
كيس كمبيوتر	DELL 5090	17W21N3	العمليات
كيس كمبيوتر	DELL 5090	36W21N3	سلمي احمد سمير كامل السبنسي
كيس كمبيوتر	DELL 5090	8XW21N3	عمرو محمد احمد ابراهيم
كيس كمبيوتر	DELL 5090	D5W21N3	محمد صبري ابو المجد
كيس كمبيوتر	DELL 5090	C5W21N3	مي احمد عبد العزيز احمد
كيس كمبيوتر	DELL 5090	F5W21N3	هشام عبد الوهاب محمد الشناوي
كيس كمبيوتر	DELL 5090	C6W21N3	وليد محمد حنفي محمود
كيس كمبيوتر	DELL 7010	C58R5W1
كيس كمبيوتر	DELL 7010	G88R5W1
كيس كمبيوتر	DELL 7010	J88R5W1
كيس كمبيوتر	DELL 7010	F38R5W1
كيس كمبيوتر	DELL 7010	GD8R5W1	عصام عبد الفتاح حسن
كيس كمبيوتر	DELL 7010	F58R5W1	عصام عبد المنعم محمد عربي
كيس كمبيوتر	DELL 7010	GF8R5W1	هند شريف حسن الدري
كيس كمبيوتر	DELL 7010	JQ23WS1	وليد محمد احمد صالح
كيس كمبيوتر	DELL 7010	368R5W1	محمد السيد ابراهيم عبد العال
كيس كمبيوتر	DELL 7010	8G8R5W1	محمد محمد جلال عبد الوهاب الخطيب
كيس كمبيوتر	DELL 7010	9W7R5W1	مخزن
كيس كمبيوتر	DELL 7010	B78R5W1	مخزن
كيس كمبيوتر	DELL 7020	4F3V574	احمد السعيد احمد حسن
كيس كمبيوتر	DELL 7020			احمد محمد جابر محمود
كيس كمبيوتر	DELL 7020	12QBH94	امل السعيد احمد حسن
كيس كمبيوتر	DELL 7020	J7QBA94	محمد جابر احمد محمد الحفناوي
كيس كمبيوتر	HP	CZC8485NM	اماني محمود محمد جمعة
كيس كمبيوتر	HP	CZC0507C9H	خالد احمد عطية محمود عطية
كيس كمبيوتر	HP	CZC84850XQ	خالد محمد السباعي عبد الحميد الغرباوي
كيس كمبيوتر	HP	TRF25107WW	سالي محمد بهجت عبد الخالق محمد
كيس كمبيوتر	HP	CZC11232K4	عميد/ حسام الدين محمد سيد علي
كيس كمبيوتر	HP	CZC848511F	كريمة عبد الحميد احمد سليمان
كيس كمبيوتر	HP	CZC0507CCG	مخزن
كيس كمبيوتر	HP	CZCQ507CDD	مخزن
كيس كمبيوتر	HP	CZC8457NVY	نقل
كيس كمبيوتر	HP	CZC11834MH	نيبال مدحت محمد عقل
كيس كمبيوتر	HP	MXL12917VK
كيس كمبيوتر	HP 6000	CZC11232K7	دعاء محمد علي حسن
كيس كمبيوتر	HP 8100	CZC111968V	امير يس محمد حسن
كيس كمبيوتر	HP COMPAQ	CZC0507CC0	اميرة ابراهيم احمد عبد الوهاب
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC0507CCS	طارق عبد القادر حسن علي حسن
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC8457NJ2	علي عبد الرحيم عبد الواحد عيد
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC0507CPR	سوزان محمد مدحت عبد المجيد الطويل
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC5170R87	محمد خميس على عثمان
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC0507C9H	محمد صبري ابو المجد
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC0507CC0	مرتجع
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC0507CDC	مرتجع
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC0507CCD	نيبال مدحت محمد عقل
كيس كمبيوتر	HP COMPAQ DX 2000MT	CZC0507CC9
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838T	حسن عبد السلام السيد سلام
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC6068392	محمد حسين شعبان محمد
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838H	محمد عبد المنعم علي محمد
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606839K	ممدوح احمد على الخولي
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838Y	ناصر ابراهيم ابراهيم محمد
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683B1	نهي محمد سعيد
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606839W	همت محمد ابو العزايم مصطفي وهبة
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606839B	وليد محمود حنفي محمود احمد
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683D6	اسامة محمود مشيمش ابراهيم
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606839X	اسلام سامي محمد فوزي
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838Y	تامر محمد علي احمد
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BV	جيهان محمد عبد السلام سليم
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838G	رضا محمد محمد سليمان
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BZ	ريهام حسين محمد عويضة
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606839F	شريف الكومي علي صالح
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838N	شوق محمد محمد جمعة
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683B3	صابرين محمد محمود محمد السمان
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC6068390	عماد الصاوى محمد الصاوى
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838J	عمرو احمد عبد الباسط احمد خليفة
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BG	عمرو محمد احمد ابراهيم
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BT	عمرو محمد احمد ابراهيم
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BM	غادة عبد الوهاب عبد العزيز الهابط
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606839V	متولي محمود ابراهيم
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BL	محمد حسني احمد احمد سكر
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606839P	محمد محمد سعيد محمد توفيق حنفي
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BF	محمد محمود عبد اللطيف جاد
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838K	مخزن
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683GH	مخزن
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838M	مخزن
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BQ	مرتجع
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683B9	مرتجع
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838Z	مروة مصطفي عبد الحليم زيدان
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838D	مريم نبيل محمود الشربيني
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BR	منصور محمد مبروك جاد الله
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683BD	مها علي شلبي عبد الرحمن
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC6068396	مي عبد المنعم محمود عراقى السيد شعبان
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838Z	نجلاء صلاح عبد الرحمن يوسف
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC6068391	ندا خميس عواد عودة
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683B5	نقل
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC60683B0	نهلة مصطفي والي
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838F
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838Q
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606839R
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC606838R	ياسر انور جابر محمد
كيس كمبيوتر	HP ELIT DESK 800 GT TOWER	CZC6068394	يمني مصطفي ياقوت حسين
كيس كمبيوتر	HP PRO 3120	CZC0507CB5
كيس كمبيوتر	HP PRO 3500	TRF251089T	ابراهيم علي بسيوني
كيس كمبيوتر	HP PRO 3500	TRF25109J5	امير فتحي محمد السيد
كيس كمبيوتر	HP PRO 3500	TRF251062Z	ايمان عادل كمال الجويلي
كيس كمبيوتر	HP PRO 3500	TRF2510924	دينا مصطفي عبدة مصطفي
كيس كمبيوتر	HP PRO 3500	TRF25107NM	عبد الحميد محمد عبد الظاهر
كيس كمبيوتر	HP PRO 3500	TRF251087C	علي محمد رجب عمران
كيس كمبيوتر	HP PRO 3500	TRF251086X	محمد حسين شعبان محمد
كيس كمبيوتر	HP PRO 3500	TRF251096Y	مروة فهمي رسلان عوض الله
كيس كمبيوتر	HP PRO 3500	TRF251099H	مصطفي سعيد صبحي عبد العزيز ابو عميرة
كيس كمبيوتر	HP PRO 3500	TRF25109FJ	احمد جمال متولي حسن
كيس كمبيوتر	HP PRO 3500	TRF25107P8	انجي محمود حلمي عوض
كيس كمبيوتر	HP PRO 3500	TRF25109QZ	بسمة نبيل احمد محمد حسن
كيس كمبيوتر	HP PRO 3500	TRF25109F7	سحر احمد عبد الحميد نافع
كيس كمبيوتر	HP PRO 3500	TRF25107W	شيماء محمود عبد الفتاح السباع
كيس كمبيوتر	HP PRO 3500	TRF251088V	شيماء محمود عبد الفتاح السباع
كيس كمبيوتر	HP PRO 3500	TRF25109JW	عادل ابراهيم الدسوقي عيد
كيس كمبيوتر	HP PRO 3500	TRF251061B	غادة احمد احمد عمارة
كيس كمبيوتر	HP PRO 3500	TRF25107PD	ماجدة محمد ابو المجد محمود
كيس كمبيوتر	HP PRO 3500	TRF251089T	مخزن
كيس كمبيوتر	HP PRO 3500	TRF25109PJ	هبة ابراهيم السيد محمود
كيس كمبيوتر	HP PRO 3500	TRF25107Z3
كيس كمبيوتر	HP PRO 3500	TRF25108DX	وليد محمد عبد الحميد الشرقاوي
كيس كمبيوتر	HP PRP 3500	TRF25107T9	ميادة احمد سيد احمد الدفراوي
كيس كمبيوتر	HP8100	CZC111968Z	محمد سيد شحاتة عبد المجيد
كيس كمبيوتر	HP8100	CZC1119698	اماني محمد السعيد عبد الستار لطفي
كيس كمبيوتر	HP8100	CZC111969J	رحاب السيد محمد محمود ابو الفضل
كيس كمبيوتر	HP8100	CZC111969C	شيماء محمد حنفي
كيس كمبيوتر	HP8100	CZC111968Y	محمد فاضل جاسر محمود
كيس كمبيوتر	HP8100	CZC1119695	مخزن
كيس كمبيوتر	HP8100	CZC111969M	مصطفي محمود انور
كيس كمبيوتر	HP8100	CZC1119692	نقل
كيس كمبيوتر	HP8100	CZC111969F	نقل
كيس كمبيوتر	بلوتو	بدون	احمد عبد الرحيم محمد عبد الرحيم
كيس كمبيوتر	بلوتو	NA	احمد محمد مكاوي يوسف
كيس كمبيوتر	بلوتو	NA	بسنت نعيم حسن محمد
كيس كمبيوتر	بلوتو	NA	حسناء محمد رمضان الطاروطي
كيس كمبيوتر	بلوتو	NA	شيماء عادل حسن حسني حافظ
كيس كمبيوتر	بلوتو	بدون	محمد محمد الشحات عبد الفتاح شلبي
كيس كمبيوتر	بلوتو	بدون	هالة محمد عبد الله اسماعيل
كيس كمبيوتر	بلوتو	NA	ياسر محمد صلاح
كيس كمبيوتر	بلوتو	NA	شيماء السيد حسين سلامة
كيس كمبيوتر	بلوتو	NA	غادة تمام عبد العزيز تمام
كيس كمبيوتر	بلوتو	N/A	محمد منصور سعيد حسن
كيس كمبيوتر	بلوتو	NA	مخزن
كيس كمبيوتر	بلوتو	NA	مخزن
كيس كمبيوتر	بلوتو	NA	منى عادل ابراهيم عثمان
كيس كمبيوتر	تجميع	2024	احمد سليمان احمد سليمان
كيس كمبيوتر	تجميع	2024	شيريهان عصمت احمد هلالي
كيس كمبيوتر	تجميع	قديم	كريم جمال محمد
كيس كمبيوتر	تجميع	2024	محمد صبري ابو المجد
كيس كمبيوتر	تجميع	قديم	مخزن
كيس كمبيوتر	تجميع	2024	نرمين محمود احمد
كيس كمبيوتر	تجميع  قديم	بدون	كريم عبد الرحمن حسن احمد الدهيني
كيس كمبيوتر	تجميع 1/2024	2024	زينب صالح فؤاد
كيس كمبيوتر	تجميع 1/2024	2024	كرم طلعت عبد الحليم دغيدي
كيس كمبيوتر	تجميع 1/2024	2024	ياسمين نبيل محمد عرفة	محمد خميس عثمان
كيس كمبيوتر	تجميع 2/2024	2024	فاتن سيد احمد
كيس كمبيوتر	تجميع 2/2024	2024	كريم حسني عبد العزيز الطيار
كيس كمبيوتر	تجميع 2024	2024	مروة حافظ عبدة حافظ
كيس كمبيوتر	سيمنز	YKDU068796	مرتجع
كيس كمبيوتر	فيجستو	YV7R003327	ايناس وجدي عبد المنعم محمد
كيس كمبيوتر	فيجستو	YLBQ003335	تامر انور سعد محمود الملاح
كيس كمبيوتر	فيجيتسو	YLPQ003297	احلام عزت محمد سالم
كيس كمبيوتر	فيجيتسو	YLPQ003298	محمد عبد الغفار يس
كيس كمبيوتر	فيجيتسو	Z352	مرتجع
كيس كمبيوتر	كيس تجميع	2024	رحاب محمد السيد عبد المنعم
كيس كمبيوتر	كيس تجميع	2024	وسام محمد عبد الله احمد
كيس كمبيوتر	كيس تجميع 1/2024	2024	دعاء جلال قرة
كيس كمبيوتر	كيس تجميع 1/2024	2024	عميد هشام منسي
كيس كمبيوتر	كيس تجميع 2/2024	2024	يسرا احمد حسن الشعراوى
كيس كمبيوتر	كيس ديل 7020	عمرو عبدالرازق عبد العظيم
"""

def run_import():
    print("⏳ جاري تهيئة قاعدة البيانات...")
    initialize_database()
    session = SessionLocal()

    # 1. إنشاء الفئة
    cat = session.query(Category).filter_by(name="كيس كمبيوتر").first()
    if not cat:
        cat = Category(name="كيس كمبيوتر", code="CAT-PC")
        session.add(cat)
        session.commit()

    # 2. إنشاء إذن الإضافة (الشراء) - لو مش موجود
    doc_in = session.query(Document).filter_by(doc_number="INIT-PC-001").first()
    if not doc_in:
        doc_in = Document(doc_type="IN", doc_number="INIT-PC-001", doc_date=date.today(), notes="جرد أولي - إضافة")
        session.add(doc_in)
        session.commit()

    # 3. إنشاء إذن الصرف (العهد) - لو مش موجود
    doc_out = session.query(Document).filter_by(doc_number="INIT-PC-002").first()
    if not doc_out:
        doc_out = Document(doc_type="OUT", doc_number="INIT-PC-002", doc_date=date.today(), notes="جرد أولي - صرف عهد")
        session.add(doc_out)
        session.commit()

    employees_cache = {}
    lines = [line.strip() for line in raw_data.strip().split("\n") if line.strip()]
    
    added_count = 0
    for idx, line in enumerate(lines):
        parts = line.split("\t")
        if len(parts) < 3: continue
        
        cat_name = parts[0]
        model = parts[1]
        serial = parts[2].strip() if parts[2] else f"SN-{idx}"
        
        # لو السيريال فاضي أو "بدون" نعمله سيريال وهمي
        if serial in ["", "بدون", "NA", "N/A", "2024", "قديم"]:
            serial = f"NO-SN-{idx}"

        emp_name = parts[3].strip() if len(parts) > 3 else ""

        # تخطي الأجهزة اللي في المخزن
        if emp_name in ["مرتجع", "مخزن", "نقل"]:
            continue
        if not emp_name: 
            continue

        # ✅ البحث عن الصنف بكود السيريال
        item = session.query(Item).filter_by(code=serial).first()
        
        # لو الصنف مش موجود، نعمله ونضيفه للمخزن (حركة وارد)
        if not item:
            item = Item(code=serial, name=f"{cat_name} {model}", category_id=cat.id, unit="قطعة", min_qty=0)
            session.add(item)
            session.flush()

            # إضافة حركة "وارد" (شراء) مرة واحدة بس
            trx_in = Transaction(document_id=doc_in.id, item_id=item.id, quantity=1, price=0, notes="جرد أولي - إضافة")
            session.add(trx_in)

        # إنشاء الموظف لو مش موجود
        if emp_name not in employees_cache:
            emp = session.query(Employee).filter_by(name=emp_name).first()
            if not emp:
                emp = Employee(name=emp_name, code=f"EMP-{len(employees_cache)+1:03d}")
                session.add(emp)
                session.flush()
            employees_cache[emp_name] = emp.id

        emp_id = employees_cache[emp_name]

        # ✅ إضافة حركة "صادر" (عهدة) - لو مش مضافة قبل كده للموظف ده
        existing_trx = session.query(Transaction).filter_by(document_id=doc_out.id, item_id=item.id).first()
        if not existing_trx:
            trx_out = Transaction(document_id=doc_out.id, item_id=item.id, quantity=1, price=0, notes="جرد أولي - صرف عهدة")
            session.add(trx_out)
            
            # ربط الموظف بالإذن
            doc_out.employee_id = emp_id
            added_count += 1

        if added_count % 10 == 0 and added_count > 0:
            session.commit()

    session.commit()
    session.close()
    print(f"🎉 اكتمل الاستيراد! تم إضافة {added_count} جهاز وربطهم بالعهد بنجاح.")

if __name__ == "__main__":
    run_import()