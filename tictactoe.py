from tkinter import *
from re import *
from itertools import combinations
import random
import time

root = Tk()
root.geometry('600x600')
root.configure(background='grey')

board = Canvas(root, width=450, height=450, bg='black')
board.place(x=75, y=75)

board.create_line(150, 0, 150, 450, width=5, fill='#fff3f4')
board.create_line(300, 0, 300, 450, width=5, fill='#fff3f4')
board.create_line(0, 150, 450, 150, width=5, fill='#fff3f4')
board.create_line(0, 300, 450, 300, width=5, fill='#fff3f4')

counter = 0

WIN_POSSIBILITIES = (
    ['x0y0', 'x0y1', 'x0y2'], ['x1y0', 'x1y1', 'x1y2'], ['x2y0', 'x2y1', 'x2y2'], ['x0y0', 'x1y0', 'x2y0'],
    ['x0y1', 'x1y1', 'x2y1'], ['x0y2', 'x1y2', 'x2y2'], ['x0y0', 'x1y1', 'x2y2'], ['x0y2', 'x1y1', 'x2y0']
)

game_history = []

FIELDS_VOCABULARY = {
    'x0y0': 1, 'x0y1': 2, 'x0y2': 3, 'x1y0': 4, 'x1y1': 5, 'x1y2': 6, 'x2y0': 7, 'x2y1': 8, 'x2y2': 9,
}

WIN_POSSIBILITIES_FIELDS = [[FIELDS_VOCABULARY[wp[0]], FIELDS_VOCABULARY[wp[1]], FIELDS_VOCABULARY[wp[2]]] for wp in
                            WIN_POSSIBILITIES]

X_Y_COORDS = {
    1: (1, 1), 2: (2, 1), 3: (3, 1), 4: (1, 2), 5: (2, 2), 6: (3, 2), 7: (1, 3), 8: (2, 3), 9: (3, 3)
}


def draw_win_line(win_condition):
    if win_condition == WIN_POSSIBILITIES[0]:
        board.create_line(10, 75, 440, 75, width=10, fill='yellow')
    if win_condition == WIN_POSSIBILITIES[1]:
        board.create_line(10, 225, 440, 225, width=10, fill='yellow')
    if win_condition == WIN_POSSIBILITIES[2]:
        board.create_line(10, 375, 440, 375, width=10, fill='yellow')
    if win_condition == WIN_POSSIBILITIES[3]:
        board.create_line(75, 10, 75, 440, width=10, fill='yellow')
    if win_condition == WIN_POSSIBILITIES[4]:
        board.create_line(225, 10, 225, 440, width=10, fill='yellow')
    if win_condition == WIN_POSSIBILITIES[5]:
        board.create_line(375, 10, 375, 440, width=10, fill='yellow')
    if win_condition == WIN_POSSIBILITIES[6]:
        board.create_line(10, 10, 440, 440, width=10, fill='yellow')
    if win_condition == WIN_POSSIBILITIES[7]:
        board.create_line(10, 440, 440, 10, width=10, fill='yellow')


def create_combinations(object_to_handle):
    res = None
    if isinstance(object_to_handle, list):
        res = combinations(object_to_handle, 3)
    return list(res)


def result():
    data_x_table = []
    data_o_table = []
    xxx = board.find_withtag('X')
    for x in xxx:
        tags = board.itemcget(x, 'tags')
        text = re.search(r'x\dy\d', tags)
        if text.group() not in data_x_table:
            data_x_table.append(text.group())
    ooo = board.find_withtag('O')
    for o in ooo:
        tags = board.itemcget(o, 'tags')
        text = re.search(r'x\dy\d', tags)
        if text.group() not in data_o_table:
            data_o_table.append(text.group())

    x_combinations = create_combinations(data_x_table)
    for x in x_combinations:
        if sorted(list(x)) in WIN_POSSIBILITIES:
            draw_win_line(sorted(list(x)))
            print('X Won!')
            board.unbind('<1>')
            return True
    o_combinations = create_combinations(data_o_table)
    for o in o_combinations:
        if sorted(list(o)) in WIN_POSSIBILITIES:
            print('O Won!')
            draw_win_line(sorted(list(o)))
            board.unbind('<1>')
            return True
    return False


def draw_shape(x, y, color='black'):
    global counter

    for i in range(0, 3):
        for j in range(0, 3):
            if (j * 150) < x < (j + 1) * 150 and (i * 150) < y < (i * 150) + 150:
                state = board.find_withtag('x{}y{}'.format(i, j))
                if not state:
                    if counter % 2 == 0:
                        game_history.append(f'X* x{i}y{j}')
                        board.create_line((j * 150) + 20, (i * 150) + 20, (j * 150) + 130, (i * 150) + 130, width=10,
                                          fill='darkred', tags=('X', 'x{}y{}'.format(i, j)))
                        board.create_line((j * 150) + 20, (i * 150) + 130, (j * 150) + 130, (i * 150) + 20, width=10,
                                          fill='darkred')
                    else:
                        game_history.append(f'O* x{i}y{j}')
                        board.create_oval((j * 150) + 20, (i * 150) + 20, (j * 150) + 130, (i * 150) + 130,
                                          fill='black', width=10, outline=color,
                                          tags=('O', 'x{}y{}'.format(i, j)))

                    counter += 1


def change_objects_color(objects, color='red', outline=None):
    if isinstance(objects, (tuple, list)):
        for item in objects:
            if outline:
                print()
                board.itemconfig(item, outline=outline)
            else:
                board.itemconfig(item, fill=color)


def display_oval():
    change_objects_color(board.find_withtag('O'), 'black', 'darkblue')


def create_oval():
    condition = len(board.find_withtag('O')) + 1
    while condition != len(board.find_withtag('O')):
        xc = random.randint(1, 4) * 144
        yc = random.randint(1, 4) * 144
        draw_shape(xc, yc, 'darkblue')
    result()
    if result():
        board.unbind('<3>')


def two_player_game(event):
    x = event.x
    y = event.y
    draw_shape(x, y, 'darkblue')
    if result():
        print(game_history)


def one_player_game(event):
    x = event.x
    y = event.y
    draw_shape(x, y)
    if result():
        board.unbind('<3>')
        return
    board.after(1000, create_oval)
    if result():
        board.unbind('<3>')
        return
    print(len(board.find_withtag('X')) + len(board.find_withtag('O')))


def preventing_x_win():
    x_list = []
    o_list = []
    for x in board.find_withtag('X'):
        x_tags = board.itemcget(x, 'tags')
        x_list.append(FIELDS_VOCABULARY[x_tags.split()[1]])
    for o in board.find_withtag('O'):
        o_tags = board.itemcget(o, 'tags')
        o_list.append(FIELDS_VOCABULARY[o_tags.split()[1]])
    condition = len(board.find_withtag('O')) + 1
    while condition != len(board.find_withtag('O')):

        xc = random.randint(1, 4) * 144
        yc = random.randint(1, 4) * 144
        if x_list == [5]:
            i = random.choice((1, 3, 7, 9))
            xc = X_Y_COORDS[i][0] * 111
            yc = X_Y_COORDS[i][1] * 111
        elif len(x_list) == 1:
            xc = X_Y_COORDS[5][0] * 111
            yc = X_Y_COORDS[5][1] * 111
        for possibility in WIN_POSSIBILITIES_FIELDS:
            for i in range(0, 3):
                if possibility[i - 2] in o_list and possibility[i - 1] in o_list and possibility[i] not in x_list:
                    xc = X_Y_COORDS[possibility[i]][0] * 111
                    yc = X_Y_COORDS[possibility[i]][1] * 111
                elif possibility[i - 2] in x_list and possibility[i - 1] in x_list and possibility[i] not in o_list:
                    xc = X_Y_COORDS[possibility[i]][0] * 111
                    yc = X_Y_COORDS[possibility[i]][1] * 111

        draw_shape(xc, yc, 'darkblue')
    result()
    if result():
        board.unbind('<3>')


def smart_computer_game(event):
    x = event.x
    y = event.y
    draw_shape(x, y)
    if result():
        board.unbind('<3>')
        return
    board.after(1000, preventing_x_win)


board.bind('<1>', two_player_game)
board.bind('<2>', one_player_game)
board.bind('<3>', smart_computer_game)

root.mainloop()
