#!/usr/bin/env python3
import readline
import os

class MyCompleter(object):  # Custom completer
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

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                if text.startswith('./'):
                    self.options = os.listdir()
                    print(self.options)
                else:
                    self.options = self.find_matches()
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options
        # return match indexed by state
        try:
            return self.matches[state]
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
