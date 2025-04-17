import pyodbc
import Auth
from tabulate import tabulate
import curses
import threading
import time

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


# define the menu function
def menu(title, classes, color='white'):
    # define the curses wrapper
    def character(stdscr, ):
        attributes = {}
        # stuff i copied from the internet that i'll put in the right format later
        icol = {
            1: 'red',
            2: 'green',
            3: 'yellow',
            4: 'blue',
            5: 'magenta',
            6: 'cyan',
            7: 'white'
        }
        # put the stuff in the right format
        col = {v: k for k, v in icol.items()}

        # declare the background color

        bc = curses.COLOR_BLACK

        # make the 'normal' format
        curses.init_pair(1, 7, bc)
        attributes['normal'] = curses.color_pair(1)

        # make the 'highlighted' format
        curses.init_pair(2, col[color], bc)
        attributes['highlighted'] = curses.color_pair(2)

        # handle the menu
        c = 0
        option = 0
        while c != 10:

            stdscr.erase()  # clear the screen (you can erase this if you want)

            # add the title
            stdscr.addstr(f"{title}\n", curses.color_pair(1))

            # add the options
            for i in range(len(classes)):
                # handle the colors
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']

                # actually add the options

                stdscr.addstr(f'> ', attr)
                stdscr.addstr(f'{classes[i]}' + '\n', attr)
            c = stdscr.getch()

            # handle the arrow keys
            if c == curses.KEY_UP and option > 0:
                option -= 1
            elif c == curses.KEY_DOWN and option < len(classes) - 1:
                option += 1
        return option

    return curses.wrapper(character)


def check_orders_background():
    while True:
        cursor.execute('''
            UPDATE orders
            SET status = 'completed'
            WHERE status = 'pending'
            AND DATEDIFF(SECOND, ordered_at, GETDATE()) >= 300;
        ''')
        cursor.commit()
        time.sleep(60)


thread = threading.Thread(target=check_orders_background, daemon=True)


class BuyBook:
    @staticmethod
    def create_order(user_id):
        cart = {}  # product_id: quantity

        def show_cart():
            if not cart:
                print("\n🛒 Savatcha bo‘sh.")
                return

            table = []
            total_sum = 0
            for book_id, quantity in cart.items():
                cursor.execute("SELECT title, price FROM books WHERE id = ?", (book_id,))
                book = cursor.fetchone()
                if book:
                    title, price = book
                    total = price * quantity
                    total_sum += total
                    table.append([book_id, title, quantity, price, total])

            headers = ["Product ID", "Kitob nomi", "Quantity", "Price", "Total"]
            print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
            print(f"\n💰 Umumiy summa: {total_sum} so'm\n")

            # Savatchadan mahsulot o‘chirish
            while True:
                remove = input("Mahsulot o‘chirmoqchimisiz? (product_id yozing yoki Enter): ").strip()
                if not remove:
                    break
                if remove.isdigit():
                    remove_id = int(remove)
                    if remove_id in cart:
                        del cart[remove_id]
                        print(f"🗑 Mahsulot ID {remove_id} savatchadan o‘chirildi.")
                        show_cart()
                    else:
                        print("❌ Bunday ID savatchada yo‘q.")
                else:
                    print("⚠️ Faqat ID kiriting yoki Enter bosing.")

        while True:
            print("\n--- Buyurtma Menyusi ---")
            print("1️⃣ Mahsulot qo‘shish")
            print("2️⃣ Savatchani ko‘rish")
            print("3️⃣ Buyurtmani yakunlash")
            print("0️⃣ Ortga qaytish")

            command = input("Tanlang (1/2/3/0): ").strip()

            if command == '0':
                print("🔙 Ortga qaytdingiz. Savatcha saqlanmoqda.")
                break

            elif command == '2':
                show_cart()

            elif command == '3':
                if not cart:
                    print("⚠️ Savatcha bo‘sh. Buyurtma yaratib bo‘lmaydi.")
                    continue

                show_cart()
                confirm = input("Tasdiqlaysizmi? (ha/yo‘q): ").strip().lower()
                if confirm != 'ha':
                    print("❌ Buyurtma bekor qilindi.")
                    continue

                # Buyurtma yaratish
                total_amount = 0
                for pid, qty in cart.items():
                    cursor.execute("SELECT price FROM books WHERE id = ?", (pid,))
                    total_amount += cursor.fetchone()[0] * qty

                cursor.execute('''
                    INSERT INTO orders (user_id, total_amount, status, ordered_at)
                    VALUES (?, ?, 'pending', GETDATE());
                ''', (user_id, total_amount))
                cursor.execute('SELECT SCOPE_IDENTITY()')
                order_id = cursor.fetchone()[0]

                for pid, qty in cart.items():
                    cursor.execute('''
                        INSERT INTO order_items (order_id, book_id, quantity, price)
                        SELECT ?, ?, ?, price FROM books WHERE id = ?;
                    ''', (order_id, pid, qty, pid))

                cursor.commit()
                cart.clear()
                print("✅ Buyurtma bazaga saqlandi (pending holatda)!")

            elif command == '1':
                try:
                    product_id = int(input("Product ID: ").strip())
                    quantity = int(input("Quantity: ").strip())
                except ValueError:
                    print("⚠️ Noto‘g‘ri format.")
                    continue

                if quantity <= 0:
                    print("⚠️ Miqdor musbat bo‘lishi kerak.")
                    continue

                cursor.execute('SELECT title, stock_qty FROM books WHERE id = ?', (product_id,))
                book = cursor.fetchone()
                if book is None:
                    print("❌ Kitob topilmadi.")
                    continue

                title, stock_qty = book
                if quantity > stock_qty:
                    print(f"❗ Faqat {stock_qty} dona mavjud.")
                    continue

                if product_id in cart:
                    cart[product_id] += quantity
                else:
                    cart[product_id] = quantity

                print(f"✅ Savatchaga qo‘shildi: {quantity} ta '{title}'")

            else:
                print("⚠️ Noto‘g‘ri tanlov. Qayta urinib ko‘ring.")

    @staticmethod
    def decline_order():
        query = ''' exec dbo.get_user_p_orders ? '''
        cursor.execute(query, Auth.Auth.info['user_email'])
        rows = cursor.fetchall()
        if rows:
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            menu_options = [str(i[0]) + ' - product' for i in rows]
            selected_index = menu('Choose product: ', menu_options, 'blue')
            selected_id = rows[selected_index][0]
            cancel_query = ''' exec dbo.cancel_orders ? '''
            cursor.execute(cancel_query, (selected_id,))
            print(f"Order with ID {selected_id} has been canceled.")
            connection.commit()
        else:
            print("Sizda bekor qilishingiz mumkin bo'lgan zakazlar yo'q")

    @staticmethod
    def see_orders():
        query = ''' exec dbo.get_user_orders ? '''
        result = cursor.execute(query, (Auth.Auth.info['user_email'],))
        if result:
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print('Zakazlar topilmadi ❗')


if __name__ == "__main__":
    thread.start()
