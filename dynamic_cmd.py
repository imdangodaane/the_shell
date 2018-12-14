#!/usr/bin/env python3
import readline
import os
import re


class MyCompleter(object):
    def __init__(self):
        self.options = []

    def find_matches(self):
        options = []
        try:
            paths = os.environ['PATH'].split(':')
            for path in paths:
                try:
                    options += os.listdir(path)
                except FileNotFoundError:
                    continue
            return options
        except KeyError:
            pass

    def find_path_from_buffer(self, buffer):
        pattern = re.compile('.*/')
        return pattern.search(buffer).group()

    def complete(self, text, state):
        self.options = self.find_matches()
        buffer = readline.get_line_buffer()

        if buffer:
            if buffer.startswith('.'):
                try:
                    path = self.find_path_from_buffer(buffer)
                    self.options = os.listdir(path)
                except FileNotFoundError:
                    self.options = []
        else:
            self.options = []

        if state == 0:
            if text:
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options
        try:
            return self.matches[state] + ' '
        except IndexError:
            return None


def dynamic_cmd_complete():
    try:
        paths = os.environ['PATH'].split(':')

    except KeyError:
        pass
    completer = MyCompleter()
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

    _input = input("Input: ")
    print("You entered", _input)


def main():
    dynamic_cmd_complete()


if __name__ == '__main__':
    main()
