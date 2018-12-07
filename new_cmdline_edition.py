#!/usr/bin/env python3
import curses
import sys


class MyBelovedScreen:
    def __init__(self):
        self.cmd = ''
        self.cmd_list = []
        self.cmd_ls_char = []
        self.cmd_len = 0
        self.cmd_lines = 1
        self.std_deviation = 10
        self.lines = 1
        self.win_height = 0
        self.win_width = 0
        self.current_y = 0
        self.home_y = 0
        self.current_x = 0
        self.index_x = 0
        self.delta = 0
        self.key_pressed = -1
        self.screen = self.screen_init()
        self.screen_operate()
        self.screen_terminate()

    def screen_init(self):
        screen = curses.initscr()
        # curses.echo()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        # screen.nodelay(True)
        return screen

    def screen_terminate(self):
        # curses.noecho()
        curses.nocbreak()
        self.screen.keypad(False)
        # screen.nodelay(False)
        curses.endwin()

    def screen_config(self):
        curses.start_color()
        curses.init_color(2, 0, 450, 0)
        curses.init_color(6, 450, 0, 0)
        curses.init_pair(1, 6, 2)
        self.screen.bkgd(curses.ACS_DIAMOND, curses.color_pair(1))
        self.screen.erase()
        self.screen.bkgdset(' ', curses.color_pair(1))

    def press_HOME(self):
        self.index_x = 0
        self.screen.move(self.home_y, self.std_deviation)

    def press_END(self):
        self.index_x = len(self.cmd_ls_char)
        width = self.std_deviation + self.cmd_len
        if width > self.win_width:
            self.screen.move(self.current_y + width // self.win_width,
                             width % self.win_width)
        else:
            self.screen.move(self.current_y, width)

    def press_LEFT(self):
        if self.index_x <= 0:
            return None
        self.index_x -= 1
        leftmost = 0
        if self.current_y - self.home_y ==  0:
            leftmost = self.std_deviation
        if self.current_x > leftmost:
            self.screen.move(self.current_y, self.current_x - 1)
        if self.current_x == 0:
            self.screen.move(self.current_y - 1, self.win_width - 1)

    def press_RIGHT(self):
        if self.index_x > len(self.cmd_ls_char) - 1:
            return None
        self.index_x += 1
        rightmost = self.std_deviation + len(self.cmd_ls_char)
        if self.current_y - self.home_y != 0:
            rightmost = len(self.cmd_ls_char)
        if self.current_x == self.win_width - 1:
            self.screen.move(self.current_y + 1, 0)
        elif self.current_x <= rightmost:
            self.screen.move(self.current_y, self.current_x + 1)

    def press_UP(self):
        pass

    def press_DOWN(self):
        pass

    def press_BACKSPACE(self):
        pass

    def press_DC(self):
        pass

    def press_RESIZE(self):
        self.screen.redrawln(0, 2)
        self.screen.refresh()

    def press_ENTER(self):
        for character in self.cmd_ls_char:
            self.cmd += character
        if self.cmd in self.cmd_list:
            pass
        elif self.cmd == 'clear':
            self.screen.clear()
            self.screen.addstr('intek-sh$ ')
        else:
            self.screen.move(self.current_y + self.lines, 0)
            self.screen.addstr(self.cmd + ': command not found')
            self.screen.move(self.current_y + self.lines + self.cmd_lines, 0)
            self.screen.addstr('intek-sh$ ')
        self.cmd = ''
        self.cmd_ls_char = []
        self.home_y, home_x = self.screen.getyx()
        self.lines = 1
        self.cmd_lines = 1
        self.index_x = 0

    def press_NORMAL_KEY(self):
        '''
        Operation handle when pressed normal key
        Config the window size when overflow
        '''
        self.cmd_ls_char.insert(self.index_x, chr(self.key_pressed))
        self.index_x += 1
        if self.screen.inch(self.current_y, self.win_width) != 18446744073709551615:
            self.screen.move(self.current_y + 1, 0)
            self.current_y, self.current_x = self.screen.getyx()
        self.screen.insstr(chr(self.key_pressed))
        if self.current_x + 1 < self.win_width:
            self.screen.move(self.current_y, self.current_x + 1)
        else:
            self.screen.move(self.current_y + 1, 0)
            self.lines += 1
        self.screen.refresh()

    def screen_operate(self):
        '''
        Screen Operation
        Init a new screen window with prompt, create some variables for
        handling command from user input
        '''
        # 18446744073709551615 = ' ' <- blank character
        self.screen.addstr('intek-sh$ ')
        while self.cmd != 'exit':
            # Find window height and width for handling user resize
            self.win_height, self.win_width = self.screen.getmaxyx()
            self.current_y, self.current_x = self.screen.getyx()
            # Find index of a char_command in cmd_ls_char
            # self.index_x = self.current_x - self.std_deviation
            self.cmd_len = len(self.cmd_ls_char)
            self.delta = 0
            self.cmd_lines = 1 + ((self.cmd_len + self.delta) // self.win_width)
            # Get key from user keyboard
            self.key_pressed = self.screen.getch()
            if self.key_pressed == curses.KEY_HOME:
                self.press_HOME()
            elif self.key_pressed == curses.KEY_END:
                self.press_END()
            elif self.key_pressed == curses.KEY_LEFT:
                self.press_LEFT()
            elif self.key_pressed == curses.KEY_RIGHT:
                self.press_RIGHT()
            elif self.key_pressed == curses.KEY_UP:
                self.press_UP()
            elif self.key_pressed == curses.KEY_DOWN:
                self.press_DOWN()
            elif self.key_pressed == curses.KEY_BACKSPACE:
                self.press_BACKSPACE()
            elif self.key_pressed == curses.KEY_DC:
                self.press_DC()
            elif self.key_pressed == 410 or self.key_pressed == curses.KEY_RESIZE:
                self.press_RESIZE()
            elif self.key_pressed == 10 or self.key_pressed == curses.KEY_ENTER:
                self.press_ENTER()
            else:
                self.press_NORMAL_KEY()


if __name__ == '__main__':
    MyBelovedScreen()
