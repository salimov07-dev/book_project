import sqlalchemy as sa
import pandas as pd
from sqlalchemy import text
from tabulate import tabulate

conn_str = (
    "mssql+pyodbc://project:qwerty123@172.25.59.2:1433/bookstore"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = sa.create_engine(conn_str)
connection = engine.connect()


class Reports:
    @staticmethod
    def monthly_reports():
        query = ''' select s1.id,s5.id,status,ordered_at,s5.price from users s1
join orders s2
on s1.id = s2.user_id
join inventory_logs s3
on s2.id = s3.id
join order_items s4
on s2.id = s4.book_id
join books s5
on s4.book_id = s5.id
where ordered_at between DATEADD(MONTH,-1,getdate()) and GETDATE()'''

        df = pd.read_sql_query(query, connection)
        df.to_csv('../Report_files/monthly_reports.csv', index=False)

    @staticmethod
    def top_buyers():
        query = text("SELECT * FROM dbo.select_top_buyers")
        result = connection.execute(query)
        rows = result.fetchall()
        headers = result.keys()
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    @staticmethod
    def top_reviewed_books():
        query = '''
    SELECT b.id, b.title, COUNT(r.rating) AS total_ratings, AVG(r.rating) AS avg_rating
    FROM books b
    JOIN reviews r ON b.id = r.book_id
    GROUP BY b.id, b.title
    ORDER BY total_ratings DESC, avg_rating DESC
'''
        df = pd.read_sql(query, engine)
        df.to_csv("top_rated_books.csv", index=False)
        print("✅ CSV fayl muvaffaqiyatli saqlandi: top_rated_books.csv")
