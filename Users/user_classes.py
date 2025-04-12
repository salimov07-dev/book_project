import pyodbc
from tabulate import tabulate

connection = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=172.25.59.2,1433"  # Yoki kompyuter nomi
    "DATABASE=BookStore;"
    "UID=project;"  # SQL Server foydalanuvchi nomi
    "PWD=qwerty123;"  # SQL Server paroli
    "TrustServerCertificate=yes;",  # Sertifikat xatolarini oldini oladi
    timeout=60
)
cursor = connection.cursor()
a = cursor.execute(''' use BookStore ''')


class Users:
    @staticmethod
    def get_all_users():
        """2.Foydalanuvchilar ro‘yxatini ko‘rish"""

        cursor.execute("SELECT id, name, email, phone FROM users")
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    @staticmethod
    def get_user():
        """3. Muayyan foydalanuvchining buyurtma tarixini ko‘rish"""
        while True:
            user_name = input(' Enter Your Name: ').lower()
            if not user_name:
                continue
            else:
                query = "exec dbo.GetUserOrders ? "
                result = cursor.execute(query, (user_name,))
                rows = cursor.fetchall()
                if not rows:
                    print(' ❌ Buyurtmalar topilmadi.')
                    break
                else:
                    headers = [desc[0] for desc in cursor.description]
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                    break


connection.commit()
