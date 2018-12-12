#!/usr/bin/env python3
import curses
import sys


class Haha:
    def __init__(self):
        self.name = self.assign_name()
        self.age = '23'
        self.run_it()

    def run_it(self):
        cmd = input()
        while cmd != 'exit':
            print(self.name, self.age)
            cmd = input()

    def assign_name(self):
        return 'Qui'


if __name__ == '__main__':
    Haha()
