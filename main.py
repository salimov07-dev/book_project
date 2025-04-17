# ---  Global Imports ---
import pyodbc
import re
from tabulate import tabulate
import curses
import pandas

# --- Local Imports ---
import Menus
import Users
import Auth
import Book
import Inventory
import Buy
import Reports

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


# define the menu function
# def menu(title, classes, color='white'):
#     # define the curses wrapper
#     def character(stdscr, ):
#         attributes = {}
#         # stuff i copied from the internet that i'll put in the right format later
#         icol = {
#             1: 'red',
#             2: 'green',
#             3: 'yellow',
#             4: 'blue',
#             5: 'magenta',
#             6: 'cyan',
#             7: 'white'
#         }
#         # put the stuff in the right format
#         col = {v: k for k, v in icol.items()}
#
#         # declare the background color
#
#         bc = curses.COLOR_BLACK
#
#         # make the 'normal' format
#         curses.init_pair(1, 7, bc)
#         attributes['normal'] = curses.color_pair(1)
#
#         # make the 'highlighted' format
#         curses.init_pair(2, col[color], bc)
#         attributes['highlighted'] = curses.color_pair(2)
#
#         # handle the menu
#         c = 0
#         option = 0
#         while c != 10:
#
#             stdscr.erase()  # clear the screen (you can erase this if you want)
#
#             # add the title
#             stdscr.addstr(f"{title}\n", curses.color_pair(1))
#
#             # add the options
#             for i in range(len(classes)):
#                 # handle the colors
#                 if i == option:
#                     attr = attributes['highlighted']
#                 else:
#                     attr = attributes['normal']
#
#                 # actually add the options
#
#                 stdscr.addstr(f'> ', attr)
#                 stdscr.addstr(f'{classes[i]}' + '\n', attr)
#             c = stdscr.getch()
#
#             # handle the arrow keys
#             if c == curses.KEY_UP and option > 0:
#                 option -= 1
#             elif c == curses.KEY_DOWN and option < len(classes) - 1:
#                 option += 1
#         return option
#
#     return curses.wrapper(character)
#
#
# print(f"output:", menu('TEST', ['this will return 0', 'this will return 1',
#                                 'this is just to show that you can do more options then just two'], 'blue'))

command_txt = ''' Enter Command Number: '''
while True:
    Menus.clean_terminal()
    Menus.store_menu()
    command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
    if command_number == 1:
        while True:
            Menus.auth_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                if not Auth.Auth.user:  # not user = kirmagan
                    Auth.Auth.register()
                else:
                    Auth.Auth.acc_details()
            elif command_number == 2:
                if not Auth.Auth.user:
                    Auth.Auth.login()
                else:
                    Auth.Auth.logout()
            elif command_number == 3:
                break
    elif command_number == 2:
        while True:
            Menus.user_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                Users.Users.get_all_users()
            elif command_number == 2:
                Users.Users.get_user()
            elif command_number == 3:
                break
    elif command_number == 3:
        while True:
            Menus.book_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                if Auth.Auth.user:
                    Book.Book.add_book()
                else:
                    Book.Book.get_books()
            elif command_number == 2:
                if Auth.Auth.user:
                    Book.Book.update_books_qty()
                else:
                    Book.Book.get_top_book()
            elif command_number == 3:
                if Auth.Auth.user:
                    Book.Book.get_books()
                else:
                    break
            elif command_number == 4:
                if Auth.Auth.user:
                    Book.Book.get_top_book()
            elif command_number == 5:
                if Auth.Auth.user:
                    query = "SELECT id FROM users WHERE email = ?"
                    user_id = cursor.execute(query, (Auth.Auth.info['user_email'],))
                    result = user_id.fetchall()
                    Book.Book.leave_feedback(result[0][0])
                else:
                    pass
            elif command_number == 6:
                if Auth.Auth.user:
                    break
    elif command_number == 4:
        while True:
            Menus.orders_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if not Auth.Auth.user:
                print(f' {Bcolors.WARNING} You Should ( Register / login) to buy a new book(s) {Bcolors.ENDC}')
            if Auth.Auth.user:
                if command_number == 1:
                    query = "SELECT id FROM users WHERE email = ?"
                    user_id = cursor.execute(query, (Auth.Auth.info['user_email'],))
                    result = user_id.fetchall()
                    Buy.BuyBook.create_order(result[0][0])
            else:
                break

            if Auth.Auth.user:
                if command_number == 2:
                    Buy.BuyBook.decline_order()
            if Auth.Auth.user:
                if command_number == 3:
                    Buy.BuyBook.see_orders()
            if Auth.Auth.user:
                if command_number == 4:
                    break
    elif command_number == 5:
        while True:
            Menus.inventory_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                Inventory.Inventory.backup_logs()
            elif command_number == 2:
                Inventory.Inventory.low_stock_books()
            elif command_number == 3:
                break
    elif command_number == 6:
        while True:
            Menus.reports_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                Reports.Reports.monthly_reports()
            elif command_number == 2:
                Reports.Reports.top_buyers()
            elif command_number == 3:
                Reports.Reports.top_reviewed_books()
            elif command_number == 4:
                break
    elif command_number == 7:
        break
cursor.close()
connection.close()
