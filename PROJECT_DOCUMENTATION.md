# 📚 الوثيقة الشاملة لنظام إدارة المخازن (MVC)

## 📌 1. نظرة عامة
- **اسم المشروع**: نظام إدارة المخازن (Warehouse Management System).
- **المطور**: AMR ABDELRAZK (AMRABDLRAZK2022@GMAIL.COM).
- **النسخة**: 2.0.0-MVC.
- **التقنية**: Python 3.14, Tkinter (واجهة), SQLAlchemy 2.0 (ORM), SQLite (قاعدة بيانات).
- **الهدف**: تحويل النظام من "البرمجة الإجرائية" إلى نمط "MVC" (Model-View-Controller) لتنظيم الكود، مع إضافة ميزات احترافية (ترخيص، صلاحيات، تقارير مالية).

---

## 🏗️ 2. هيكل المشروع (Project Structure)
تم تقسيم المشروع إلى مجلدات منفصلة:

```text
warehouse_mvc/
│
├── main.py                  ← نقطة البداية (يفحص الترخيص، يفتح شاشة الترحيب، ثم الدخول).
├── config.py                ← الإعدادات العامة (المسارات، الثوابت، معلومات المطور).
├── requirements.txt         ← المكتبات المطلوبة (SQLAlchemy, ReportLab, OpenPyXL, إلخ).
├── build.spec               ← إعدادات PyInstaller لبناء EXE.
├── license_generator.py     ← أداة المطور لتوليد أكواد التفعيل.
│
├── core/                    ← الطبقة الأساسية المشتركة
│   ├── base_model.py        ← كلاس Base لـ SQLAlchemy + Mixins (التواريخ).
│   ├── database.py          ← إعداد الاتصال بـ SQLite + Session Manager.
│   └── exceptions.py        ← استثناءات مخصصة (ValidationError, DuplicateError).
│
├── models/                  ← طبقة البيانات (SQLAlchemy Models)
│   ├── user_model.py        ← المستخدمون.
│   ├── employee_model.py    ← الموظفون.
│   ├── supplier_model.py    ← الموردون.
│   ├── warehouse_model.py   ← المخازن (بها حقل store_type: عهدة/مستهلكات).
│   ├── system_model.py      ← المنظومات.
│   ├── category_model.py    ← الفئات (التصنيفات).
│   ├── item_model.py        ← الأصناف (بها حقول: الوصف، تاريخ الصلاحية، الفئة).
│   ├── document_model.py    ← رأس الإذن (IN, OUT, RET, DIS).
│   ├── transaction_model.py ← حركات الأصناف (السطور).
│   ├── serial_model.py      ← السيريالات.
│   ├── permission_model.py  ← صلاحيات المستخدمين المخصصة.
│   └── inventory_model.py   ← الجرد الفعلي (الجرد المفاجئ).
│
├── controllers/             ← طبقة المنطق (Business Logic)
│   ├── auth_controller.py   ← المصادقة، إدارة الجلسة، فحص الصلاحيات.
│   ├── item_controller.py   ← CRUD الأصناف، البحث، توليد الكود التلقائي.
│   ├── doc_controller.py    ← إدارة الأذونات (IN/OUT/RET/DIS)، السيريالات، المرفقات.
│   ├── lookup_controller.py ← إدارة البيانات المرجعية (موظفين، موردين، مخازن).
│   ├── user_controller.py   ← إدارة المستخدمين والصلاحيات.
│   ├── category_controller.py ← إدارة الفئات.
│   ├── inventory_controller.py ← إدارة الجرد (إنشاء إذن تسوية تلقائي).
│   └── report_controller.py ← جميع التقارير (أرصدة، عهد، مالي، إلخ).
│
├── views/                   ← طبقة العرض (Tkinter)
│   ├── splash_view.py       ← شاشة الترحيب المتحركة (Canvas).
│   ├── login_view.py        ← شاشة الدخول (بطاقة أنيقة).
│   ├── main_view.py         ← النافذة الرئيسية + لوحة التحكم (Dashboard).
│   ├── sidebar_view.py      ← القائمة الجانبية (مقسمة لأقسام، بها زر الثيم).
│   ├── base_view.py         ← كلاس أساس لكل شاشات CRUD (يوفر أزرار، جدول، بحث).
│   ├── lookup_views.py      ← شاشات الموظفين، الموردين، المخازن، المنظومات.
│   ├── item_view.py         ← شاشة تعريف الأصناف.
│   ├── category_view.py     ← شاشة إدارة الفئات.
│   ├── user_view.py         ← شاشة إدارة المستخدمين (بها نافذة الصلاحيات).
│   ├── doc_view.py          ← شاشات الأذونات (IN/OUT/RET/DIS) + نافذة السطر.
│   ├── report_view.py       ← شاشة التقارير الموحدة (قائمة منسدلة).
│   ├── parent_picker.py     ← نافذة بحث ذكية (Picker) للاختيار من القوائم.
│   ├── about_view.py        ← شاشة حول البرنامج (تعرض حالة الترخيص).
│   ├── global_search_view.py ← شاشة البحث الشامل.
│   └── activation_view.py   ← شاشة التفعيل (تظهر إذا كان البرنامج غير مرخص).
│
└── utils/                   ← أدوات مساعدة
    ├── theme.py             ← الألوان والخطوط (يدعم الثيم الداكن والفاتح).
    ├── hwid.py              ← توليد البصمة (HWID) والتحقق من كود الترخيص.
    ├── password.py          ← تشفير كلمات المرور (PBKDF2).
    ├── validators.py        ← التحقق من صحة المدخلات.
    ├── ui_helpers.py        ← دوال مساعدة لبناء الواجهات (add_form_row).
    ├── excel_io.py          ← تصدير واستيراد Excel.
    └── pdf_gen.py           ← توليد ملفات PDF (تقارير، فواتير، إقرارات).