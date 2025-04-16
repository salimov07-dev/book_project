import pyodbc
import Auth
from tabulate import tabulate
import curses

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


class BuyBook:
    @staticmethod
    def create_order():
        pass

    @staticmethod
    def decline_order():
        query = ''' exec dbo.get_user_p_orders ? '''
        cursor.execute(query, Auth.Auth.info['user_email'])
        rows = cursor.fetchall()

        if rows:
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(rows, headers=headers, tablefmt="grid"))

            # Build options for the menu
            menu_options = [str(i[0]) + ' - product' for i in rows]

            # Get the index selected by the user
            selected_index = menu('Choose product: ', menu_options, 'blue')

            # Get the actual ID from the original rows using the index
            selected_id = rows[selected_index][0]

            # Cancel the order with the selected ID
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
