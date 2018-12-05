#!/usr/bin/env python3
import curses
from curses import wrapper


def main():
    stdscr = curses.initscr()
    stdscr.addstr('intek-sh$ ')
    k = stdscr.getstr().decode()
    while k != ':q':
        message = (str(k) + ': command not found\n')
        stdscr.addstr(message)
        stdscr.addstr('intek-sh$ ')
        k = stdscr.getstr().decode()
    curses.endwin()

main()

