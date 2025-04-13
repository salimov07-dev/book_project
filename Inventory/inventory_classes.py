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


class Inventory:
    @staticmethod
    def backup_logs():
        query = ''' select s1.id,s2.title,change_qty,reason,changed_at from inventory_logs s1
join books s2
on s1.book_id = s2.id '''
        result = cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        connection.commit()

    @staticmethod
    def low_stock_books():
        query = ''' select id,title,author,genre,stock_qty,price from books
where stock_qty < 10 '''
        result = cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print('Kam zaxiradagi kitoblar topilmadi')
        else:
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            connection.commit()
