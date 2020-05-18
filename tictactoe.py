from tkinter import *
from re import *
from itertools import combinations

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
    o_combinations = create_combinations(data_o_table)
    for o in o_combinations:
        if sorted(list(o)) in WIN_POSSIBILITIES:
            print('O Won!')
            draw_win_line(sorted(list(o)))
            board.unbind('<1>')


def draw_shape(event):
    x = event.x
    y = event.y
    global counter

    for i in range(0, 3):
        for j in range(0, 3):
            if (j * 150) < x < (j + 1) * 150 and (i * 150) < y < (i * 150) + 150:
                state = board.find_withtag('x{}y{}'.format(i, j))
                if not state:
                    if counter % 2 == 0:
                        board.create_line((j * 150) + 20, (i * 150) + 20, (j * 150) + 130, (i * 150) + 130, width=10,
                                          fill='darkred', tags=('X', 'x{}y{}'.format(i, j)))
                        board.create_line((j * 150) + 20, (i * 150) + 130, (j * 150) + 130, (i * 150) + 20, width=10,
                                          fill='darkred')
                    else:
                        board.create_oval((j * 150) + 20, (i * 150) + 20, (j * 150) + 130, (i * 150) + 130,
                                          fill='black', width=10, outline='darkblue',
                                          tags=('O', 'x{}y{}'.format(i, j)))

                    counter += 1
    result()


board.bind('<1>', draw_shape)

root.mainloop()