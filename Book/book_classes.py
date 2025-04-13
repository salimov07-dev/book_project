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


class Book:
    @staticmethod
    def get_books():
        query = '''select id,title,author,genre,stock_qty,price from books where stock_qty > 0 '''
        result = cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    @staticmethod
    def get_top_book():
        query = ''' select * from dbo.view_top_books '''
        result = cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        connection.commit()
    @staticmethod
    def add_book():
        book_title = input('Enter Book Name: ').strip()
        book_author = input('Enter Book Author: ').strip()
        book_genre = input('Enter Book Genre: ').strip()
        stock_qty = int(input('Enter Book Quantity: '))
        book_price = float(input('Enter Book Price: '))
        if book_title and book_author and book_genre and stock_qty and book_price:
            query = ''' exec dbo.insert_book ? , ? , ? , ? , ? '''
            result = cursor.execute(query, (book_title, book_author, book_genre, stock_qty, book_price))
            print(' Added successfully ✅')
        else:
            print(' 🚫 Fill all inputs ❗')
        connection.commit()