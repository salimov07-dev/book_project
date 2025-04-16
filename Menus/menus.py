import os
import Auth


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clean_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def store_menu():
    print(''' --- Book Store Managment Sysytem --- ''')
    print(''' 1️⃣. Auth (Tizimga kirish) 🔑 ''')
    print(''' 2️⃣. Foydalanuvchilar menyusi 👤 ''')
    print(''' 3️⃣. Kitoblar menyusi 📘 ''')
    print(''' 4️⃣. Buyurtmalar menyusi 🛒 ''')
    print(''' 5️⃣. Inventar va Ombor 🧾 ''')
    print(''' 6️⃣. Hisobotlar va Tahlil 📊 ''')
    print(''' 7️⃣. Dasturdan chiqish ❌ ''')


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
    print(''' 1️⃣. Foydalanuvchilar ro‘yxatini ko‘rish ''')
    print(''' 2️⃣. Muayyan foydalanuvchining buyurtma tarixini ko‘rish ''')
    print(''' 3️⃣. Ortga qaytish ''')


def book_menu():
    if Auth.Auth.user:
        print(''' 1️⃣. Yangi kitob qo‘shish''')
    else:
        pass
    if Auth.Auth.user:
        print(''' 2️⃣. Kitob zaxirasini yangilash(sotuv yoki qo‘shish)''')
    else:
        pass
    if Auth.Auth.user:
        print(''' 3️⃣. Mavjud kitoblar ro‘yxatini ko‘rish''')
    else:
        print(''' 1️⃣. Mavjud kitoblar ro‘yxatini ko‘rish''')
    if Auth.Auth.user:
        print(''' 4️⃣. Eng ko‘p sotilgan kitoblar ro‘yxatini chiqarish''')
    else:
        print(''' 2️⃣. Eng ko‘p sotilgan kitoblar ro‘yxatini chiqarish''')
    if Auth.Auth.user:
        print(''' 5️⃣. Ortga qaytish ''')
    else:
        print(''' 3️⃣. Ortga qaytish ''')


def orders_menu():
    if not Auth.Auth.user:
        print(f' {Bcolors.WARNING} You Should ( Register / login) to buy a new book(s) {Bcolors.ENDC}')
    if Auth.Auth.user:
        print(''' 1️⃣. Buyurtma yaratish (bir nechta kitob tanlash)''')
    else:
        pass
    if Auth.Auth.user:
        print(''' 2️⃣. Buyurtmani bekor qilish''')
    else:
        pass
    if Auth.Auth.user:
        print(''' 3️⃣. Foydalanuvchining buyurtmalar tarixini ko‘rish''')
    if Auth.Auth.user:
        print(''' 4️⃣ Ortga Qaytish ''')
    else:
        print(''' 1️⃣ Ortga Qaytish ''')


def inventory_menu():
    print(''' 1️⃣. Zaxira loglarini ko‘rish ''')
    print(''' 2️⃣. Kam zaxiradagi kitoblarni ko‘rish''')
    print(''' 3️⃣. Ortga qaytish ''')


def reports_menu():
    print(''' 1️⃣. Oylik savdo hisoboti''')
    print(''' 2️⃣. Eng ko‘p buyurtma bergan foydalanuvchini ko‘rish''')
    print(''' 3️⃣. Eng ko‘p baho olingan kitoblar ro‘yxati''')
