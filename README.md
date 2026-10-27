# FastAPI Library API

یک REST API ساده برای مدیریت کتابخانه که با **FastAPI** و **Pydantic** نوشته شده و داده‌ها را در **PostgreSQL** ذخیره می‌کند.

این پروژه به‌عنوان تمرین آموزشی ساخته شده است.

## امکانات

- دریافت لیست همه‌ی کتاب‌ها
- افزودن کتاب جدید
- دریافت اطلاعات یک کتاب با شناسه‌ی آن
- ویرایش اطلاعات کتاب با متد PATCH
- حذف کتاب
- اعتبارسنجی داده‌های ورودی با Pydantic
- برگرداندن خطای HTTP مناسب وقتی کتاب پیدا نشود
- ذخیره‌ی ماندگار داده‌ها در PostgreSQL

## تکنولوژی‌ها

- Python
- FastAPI
- Pydantic
- PostgreSQL
- psycopg
- python-dotenv
- uv

## پیش‌نیازها

- Python نسخه‌ی 3.10 یا بالاتر
- [uv](https://docs.astral.sh/uv/)
- [PostgreSQL](https://www.postgresql.org/download/)

## نصب

ابتدا ریپازیتوری را کلون کنید:

```bash
git clone https://github.com/rominaxoii/fastapi-library-api.git
cd fastapi-library-api
```

وابستگی‌ها را نصب کنید:

```bash
uv sync
```

## راه‌اندازی دیتابیس

۱. یک دیتابیس به نام `library_db` بسازید (در psql یا pgAdmin):

```sql
CREATE DATABASE library_db;
```

۲. جدول `books` را با فایل `schema.sql` بسازید:

```bash
psql -U postgres -d library_db -f schema.sql
```

اگر از pgAdmin استفاده می‌کنید، دیتابیس `library_db` را انتخاب کنید، Query Tool را باز کنید و محتوای فایل `schema.sql` را اجرا کنید.

۳. فایل `.env.example` را کپی کنید و اسم کپی را `.env` بگذارید، بعد پسورد کاربر `postgres` را داخلش بنویسید:

```
DB_PASSWORD=your_password
```

فایل `.env` در `.gitignore` قرار دارد و وارد Git نمی‌شود، پس پسورد شما در ریپازیتوری ذخیره نمی‌شود. اتصال به‌صورت پیش‌فرض به `localhost` و پورت `5432` با کاربر `postgres` انجام می‌شود (در فایل `database.py` قابل تغییر است).

## اجرای برنامه

سرور توسعه را اجرا کنید:

```bash
uv run fastapi dev main.py
```

API روی آدرس زیر در دسترس خواهد بود:

http://127.0.0.1:8000

## Endpoint ها

| متد | آدرس | توضیح | کد موفقیت |
|---|---|---|---|
| GET | `/books` | دریافت همه‌ی کتاب‌ها | 200 |
| POST | `/books` | ساخت کتاب جدید | 201 |
| GET | `/books/{book_id}` | دریافت یک کتاب با شناسه | 200 |
| PATCH | `/books/{book_id}` | ویرایش یک کتاب موجود | 200 |
| DELETE | `/books/{book_id}` | حذف یک کتاب | 200 |

اگر کتابی وجود نداشته باشد، درخواست‌های `GET` و `PATCH` و `DELETE` روی `/books/{book_id}` کد `404` برمی‌گردانند.

## مستندات تعاملی API

FastAPI به‌صورت خودکار مستندات تعاملی می‌سازد.

بعد از اجرای سرور، به آدرس زیر بروید:

http://127.0.0.1:8000/docs

از این صفحه می‌توانید همه‌ی endpoint ها را تست کنید.

## نمونه‌ی داده‌ی کتاب

نمونه‌ی بدنه‌ی JSON برای ساخت کتاب (`POST /books`):

```json
{
  "title": "The Little Prince",
  "author": "Antoine de Saint-Exupery",
  "year": 1943
}
```

نمونه‌ی بدنه‌ی JSON برای ویرایش کتاب (`PATCH /books/{book_id}`). فقط فیلدهایی که ارسال کنید تغییر می‌کنند:

```json
{
  "title": "New title"
}
```

## ساختار پروژه

```
.
├── main.py          # تعریف endpoint ها
├── database.py      # اتصال به PostgreSQL و کوئری‌های SQL
├── schema.sql       # ساخت جدول books
├── .env.example     # نمونه‌ی فایل تنظیمات (بدون پسورد واقعی)
├── pyproject.toml   # مشخصات پروژه و وابستگی‌ها
└── uv.lock          # نسخه‌ی دقیق وابستگی‌ها
```

## نگهداری داده‌ها

اطلاعات کتاب‌ها در جدول `books` در PostgreSQL ذخیره می‌شود و با خاموش و روشن شدن سرور از بین نمی‌رود. همه‌ی کوئری‌ها پارامتری هستند تا از SQL Injection جلوگیری شود.