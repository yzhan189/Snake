def draw_chr(cells, win, chr):
    # print("---------------")
    # print(cells)
    # print("---------------")
    for cell in cells:
        win.addch(cell[0], cell[1], chr)