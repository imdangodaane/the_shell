#!/usr/bin/env python3
import curses
import sys


def screen_init():
    intekscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    intekscr.keypad(True)
    # intekscr.nodely(True)
    return intekscr


def screen_terminate(screen):
    # curses.noecho()
    curses.nocbreak()
    screen.keypad(False)
    # screen.nodelay(False)
    curses.endwin()


def screen_config(screen):
    curses.start_color()
    curses.init_color(2, 0, 450, 0)
    curses.init_color(6, 450, 0, 0)
    curses.init_pair(1, 6, 2)
    screen.bkgd(curses.ACS_DIAMOND, curses.color_pair(1))
    screen.erase()
    screen.bkgdset(' ', curses.color_pair(1))


def press_HOME():
    pass


def press_END():
    pass


def press_LEFT():
    pass


def press_RIGHT():
    pass


def press_UP():
    pass


def press_DOWN():
    pass


def press_BACKSPACE():
    pass


def press_DC():
    pass


def press_RESIZE():
    pass


def press_ENTER():
    pass


def press_NORMAL_KEY(screen,
                     win_height, win_width,
                     current_y, current_x,
                     cmd_ls_char, index_x,
                     key_pressed):
    '''
    Operation handle when pressed normal key
    '''
    cmd_ls_char.insert(index_x, chr(key_pressed))
    screen.insstr(chr(key_pressed))
    if current_x + 1 < win_width:
        screen.move(current_y, current_x + 1)
    else:
        screen.move(current_y + 1, 0)
    screen.refresh()
    return cmd_ls_char


def screen_operate(screen):
    '''
    Screen Operation
    '''
    # Init a new screen window with prompt, create some variables for
    # handling command from user input
    screen.addstr("intek-sh$ ")
    cmd = ''
    cmd_ls_char = []
    std_deviation = 10  # This is the length of "intek-sh$ "
    screen_lines = 1
    while cmd != 'exit':
        # Find window height and width for handling user resize
        win_height, win_width = screen.getmaxyx()
        current_y, current_x = screen.getyx()
        # Find index of a char_command in cmd_ls_char
        index_x = current_x - std_deviation
        cmd_len = len(cmd_ls_char)
        delta = 0
        cmd_lines = 1 + ((cmd_len + delta) // win_width)
        # Get key from user keyboard
        key_pressed = screen.getch()
        if key_pressed == curses.KEY_HOME:
            press_HOME()
        elif key_pressed == curses.KEY_END:
            press_END()
        elif key_pressed == curses.KEY_LEFT:
            press_LEFT()
        elif key_pressed == curses.KEY_RIGHT:
            press_RIGHT()
        elif key_pressed == curses.KEY_UP:
            press_UP()
        elif key_pressed == curses.KEY_DOWN:
            press_DOWN()
        elif key_pressed == curses.KEY_BACKSPACE:
            press_BACKSPACE()
        elif key_pressed == curses.KEY_DC:
            press_DC()
        elif key_pressed == 410 or key_pressed == curses.KEY_RESIZE:
            press_RESIZE()
        elif key_pressed == 10 or key_pressed == curses.KEY_ENTER:
            press_ENTER()
        else:
            cmd_ls_char = press_NORMAL_KEY(screen,
                                           win_height, win_width,
                                           current_y, current_x,
                                           cmd_ls_char, index_x,
                                           key_pressed)


def main():
    intek_scr = screen_init()
    screen_operate(intek_scr)
    screen_terminate(intek_scr)


if __name__ == '__main__':
    main()
