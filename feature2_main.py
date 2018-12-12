#!/usr/bin/env python3
import curses
import sys
from curses import wrapper


def screen_init():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    # stdscr.nodelay(True)
    return stdscr


def screen_terminate(stdscr):
    # curses.noecho()
    curses.nocbreak()
    stdscr.keypad(False)
    # stdscr.nodelay(False)
    curses.endwin()


def screen_config(stdscr):
    curses.start_color()
    curses.init_color(2, 0, 450, 0)
    curses.init_color(6, 450, 0, 0)
    curses.init_pair(1, 6, 2)
    stdscr.bkgd(curses.ACS_DIAMOND, curses.color_pair(1))
    stdscr.erase()
    stdscr.bkgdset(' ', curses.color_pair(1))


def screen_operate(stdscr):
    # Init a new screen window with prompt, create some variables for
    # handling command from user input
    # stdscr = screen_init()
    # screen_config(stdscr)
    stdscr.addstr("intek-sh$ ")
    cmd = ''
    cmd_ls_char = []
    std_deviation = 10 # This is the length of "intek-sh$ "
    over_flag = False
    line = 1
    while cmd != 'exit':
        # curses.update_lines_cols()
        # stdscr.refresh()
        # stdscr.redrawwin()
        # Find window height and width for handling user resize
        win_height, win_width = stdscr.getmaxyx()
        # This process handle text on new screen window (some basic handle:
        # pressed HOME, END, LEFT/RIGHT ARROW and ENTER)
        key_pressed = stdscr.getch()

        current_y, current_x = stdscr.getyx()
        index_x = current_x - std_deviation

        cmd_len = len(cmd_ls_char)
        line_of_cmd = 1 + ((cmd_len + 19) // win_width)
        # Handle oversize command outside the window
        # Handle key press below:
        if key_pressed == curses.KEY_HOME:
            stdscr.move(current_y, std_deviation)
        elif key_pressed == curses.KEY_END:
            stdscr.move(current_y, std_deviation + cmd_len)
        elif key_pressed == curses.KEY_LEFT:
            if current_x > std_deviation:
                stdscr.move(current_y, current_x - 1)
        elif key_pressed == curses.KEY_RIGHT:
            if current_x < std_deviation + cmd_len:
                stdscr.move(current_y, current_x + 1)
        elif key_pressed == curses.KEY_UP:
            pass
        elif key_pressed == curses.KEY_DOWN:
            pass
        elif key_pressed == curses.KEY_BACKSPACE:
            if current_x > std_deviation:
                del cmd_ls_char[index_x - 1]
                stdscr.delch(current_y, current_x - 1)
        elif key_pressed == curses.KEY_DC:
            if current_x < std_deviation + cmd_len:
                del cmd_ls_char[index_x]
                stdscr.delch(current_y, current_x)
        # Handle special key when resize window
        elif key_pressed == 410: # number 410 is RESIZE KEY
            curses.update_lines_cols()
            stdscr.refresh()
            # p rint(win_height, win_width)
        elif key_pressed == curses.KEY_RESIZE:
            curses.update_lines_cols()
            stdscr.refresh()
        # Handle special key: ENTER
        elif key_pressed == 10: # number 10 is KEY_ENTER
            over_flag = False
            cmd = ''
            for i in cmd_ls_char:
                cmd += chr(i)
            cmd_ls_char = []
            if cmd == 'clear':
                stdscr.clear()
                stdscr.addstr("intek-sh$ ")
            else:
                # Handling for different command
                stdscr.move(current_y + line, 0)
                stdscr.addstr(cmd + ": command not found")
                stdscr.move(current_y + line + line_of_cmd, 0)
                stdscr.addstr("intek-sh$ ")
            line = 1
        # Handle when nothing special pressed (ASCII character)
        else:
            cmd_ls_char.insert(index_x, key_pressed)
            stdscr.insstr(chr(key_pressed))
            # if line_len > win_width - 1:
            if current_x + 2 > win_width:
                # over_flag = True
                line += 1
                stdscr.move(current_y + 1, 0)
                current_y, current_x = stdscr.getyx()
            else:
                stdscr.move(current_y, current_x + 1)
                current_y, current_x = stdscr.getyx()

    # screen_terminate(stdscr)


def cmdline_edition():
    screen_operate()


def dynamic_cmd():
    pass


def signal_handle():
    pass


def built_in_history():
    pass


def main():
    wrapper(screen_operate)


if __name__ == '__main__':
    main()
