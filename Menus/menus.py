import os
import Auth


def clean_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def store_menu():
    print(''' --- Book Store Managment Sysytem --- ''')
    print(''' 1️⃣. Auth (Tizimga kirish) 🔑 ''')
    print(''' 2️⃣. Foydalanuvchilar menyusi 👤 ''')
    print(''' 4️⃣. Kitoblar menyusi 📘 ''')
    print(''' 5️⃣. Buyurtmalar menyusi 🛒 ''')
    print(''' 6️⃣. Inventar va Ombor 🧾 ''')
    print(''' 7️⃣. Hisobotlar va Tahlil 📊 ''')
    print(''' 8️⃣. Dasturdan chiqish ❌ ''')


def auth_menu():
    if not Auth.Auth.user:
        print(''' 1️⃣. Ro‘yxatdan o‘tish (Register)''')
    if not Auth.Auth.user:
        print(''' 2️⃣. Tizimga kirish (Login)''')
    if Auth.Auth.user:
        print(''' 1️⃣. Hisob haqida malumot (Account details)''')
    if Auth.Auth.user:
        print(''' 2️⃣. Tizimdan chiqish (Logout) ''')
    if Auth.Auth.user:
        print(''' 3️⃣. Ortga qaytish ''')
    else:
        print(''' 3️⃣. Ortga qaytish ''')


def user_menu():
    print(''' 1️⃣. Yangi foydalanuvchini qo‘shish''')
    print(''' 2️⃣. Foydalanuvchilar ro‘yxatini ko‘rish ''')
    print(''' 3️⃣. Muayyan foydalanuvchining buyurtma tarixini ko‘rish ''')
    print(''' 4️⃣. Ortga qaytish ''')


def book_menu():
    print(''' 1️⃣. Yangi kitob qo‘shish''')
    print(''''2️⃣. Kitob zaxirasini yangilash(sotuv yoki qo‘shish)''')
    print(''' 3️⃣. Mavjud kitoblar ro‘yxatini ko‘rish''')
    print(''' 4️⃣. Eng ko‘p sotilgan kitoblar ro‘yxatini chiqarish''')


def orders_menu():
    print(''' 1️⃣. Buyurtma yaratish (bir nechta kitob tanlash)''')
    print(''' 2️⃣. Buyurtmani bekor qilish''')
    print(''' 3️⃣. Foydalanuvchining buyurtmalar tarixini ko‘rish''')


def inventory_menu():
    print(''' 1️⃣. Zaxira loglarini ko‘rish''')
    print(''' 2️⃣. Kam zaxiradagi kitoblarni ko‘rish''')


def reports_menu():
    print(''' 1️⃣. Oylik savdo hisoboti''')
    print(''' 2️⃣. Eng ko‘p buyurtma bergan foydalanuvchini ko‘rish''')
    print(''' 3️⃣. Eng ko‘p baho olingan kitoblar ro‘yxati''')
