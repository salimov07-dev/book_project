#  importing libarires
import pyodbc
from tabulate import tabulate
# --- import from packages ---
import Menus
import Users
import Auth

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

# qry_1 = '''  select * from users '''
# b = cursor.execute(qry_1)
# print(b.fetchall())

import curses


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
                Auth.Auth.register()
            elif command_number == 2:
                Auth.Auth.login()
            elif command_number == 3:
                Auth.Auth.logout()
            else:
                break
    elif command_number == 2:
        while True:
            Menus.user_menu()
            command_number = int(input(f'{Bcolors.BOLD + Bcolors.HEADER + command_txt + Bcolors.ENDC}'))
            if command_number == 1:
                print('''1️⃣. Yangi foydalanuvchini qo‘shish''')
            elif command_number == 2:
                Users.Users.get_all_users()
            elif command_number == 3:
                Users.Users.get_user()
            elif command_number == 4:
                break
    elif command_number == 8:
        break
cursor.close()
connection.close()
