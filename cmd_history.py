#!/usr/bin/env python3
import os
import re
from itertools import islice
from subprocess import Popen, PIPE, run
from shlex import split as shlex_split
from itertools import islice


def history_write(content):
    # Access and write content to history file (.py_history)

    history_filename = '.py_history'
    history_path = os.path.join(os.path.abspath('.'), history_filename)

    try:
        last_content = history_read(history_path, 'str').split('\n')[-2]
        if content == last_content:
            return None
    except IndexError:
        pass

    fd = os.open(history_path, os.O_CREAT | os.O_WRONLY)
    os.lseek(fd, 0, os.SEEK_END)  # Go to end of file
    # Write content
    if isinstance(content, str):
        content += '\n'
        os.write(fd, (content).encode())
    elif isinstance(content, bytes):
        content += '\n'.encode()
        os.write(fd, content)
    else:
        print("Fail to write to history file, command not type str or bytes")
        os.close(fd)
        exit(1)
    os.close(fd)


def history_read(history_path, mode):
    # Access and read content in history file (.py_history)

    fd = os.open(history_path, os.O_CREAT | os.O_RDONLY)
    if mode == 'str':
        content = os.read(fd, os.stat(history_path).st_size).decode()
    elif mode == 'byte':
        content = os.read(fd, os.stat(history_path).st_size)
    os.close(fd)
    return content


def print_history(num=None):
    # Create command function 'history' that access .py_history then output
    # a list of commands were typed prefixed with an identification number

    history_filename = '.py_history'
    history_path = os.path.join(os.path.abspath('.'), history_filename)

    previous_cmdlist = history_read(history_path, 'str').split('\n')[:-1]
    if num and '-c' in num:
        with open(history_path, 'w'):
            pass
    elif num and num.isnumeric():
    previous_cmdlist = history_read(history_path, 'str').split('\n')[:-1]
    if num and num.isnumeric():
        end = len(previous_cmdlist)
        start = end - int(num)
        if int(num) > end:
            start = 0
        for i, v in zip(range(start + 1, end + 1),
                        islice(previous_cmdlist, start, end)):
            print('{:5d} {}'.format(i, v))
    elif num and not num.isnumeric():
        print('intek-sh$: history: {}: numeric argument required'.format(num))
    else:
        for i, v in enumerate(previous_cmdlist, 1):
            print('{:5d}  {}'.format(i, v))


def print_error():
    # Print Error when there're many argument pass to ! command

    print('intek-sh$: history: too many arguments')
    exit(1)


def _double_exc(history_path):
    # Handle !! mark
    # Return end of file line
    # Return None if there's no end of file line

    try:
        return history_read(history_path, 'str').split('\n')[-2]
    except IndexError:
        return None


def _exc_posnum(history_path, num):
    # Handle !<number> mark (Ex: !3 -> return 3rd line in history file)
    # Return command correspond to positive number in history file
    # Return None if there's no command corresponding

    try:
        return history_read(history_path, 'str').split('\n')[int(num) - 1]
    except IndexError:
        return None


def _exc_negnum(history_path, num):
    # Handle !<negative number> mark (Ex: !-1 -> return final line in
    # history file)
    # Return command correspond to negative number in history file
    # Return None if there's no command corresponding

    try:
        cmd_list = history_read(history_path, 'str').split('\n')
        return cmd_list[len(cmd_list) + int(num)]
    except IndexError:
        return None


def _exc_string(history_path, string):
    # Handle !<string> mark (Ex: !c -> return the nearest line start with
    # character 'c' in history file)
    # Return False if there's no matched string in history file

    try:
        cmd_list = history_read(history_path, 'str').split('\n')
        while cmd_list:
            cmd = cmd_list.pop()
            if cmd.startswith(string):
                return cmd
    except IndexError:
        return None


def is_digit(n):
    # Return True if n is integer

    try:
        int(n)
        return True
    except ValueError:
        return False


def find_replace_of_match(history_path, match):
    # Find match of !! or !<number> or !<string> in history file

    if match == '!' or match == '-1':
        return _double_exc(history_path)
    elif is_digit(match):
        if int(match) >= 0:
            return _exc_posnum(history_path, int(match))
        else:
            return _exc_negnum(history_path, int(match))
    elif match.isalpha():
        return _exc_string(history_path, match)
    else:
        return False


def print_event_not_found(match):
    # This function print a string that show event not found with match

    print("intek-sh$ : !{}: event not found".format(match))


def find_cmd_path(cmd):
    # Find external binary path of command and return full path


    paths = os.environ['PATH']
    if paths:
        for path in paths.split(':'):
            try:
                if cmd in os.listdir(path):
                    return os.path.join(path, cmd)
            except FileNotFoundError:
                continue
        return False
    else:
        print("intek-sh$ : path: can not find PATH")


def exclamation_handle(line, built_in_functions):
    # Handle exclamation mark in command

    history_filename = '.py_history'
    history_path = os.path.join(os.path.abspath('.'), history_filename)

    result = []
    pattern = re.compile('!(!|-?\d+|\w.*)')
    matches = pattern.findall(line)

    for match in matches:
        change = find_replace_of_match(history_path, match)
        if change:
            line = line.replace('!' + match, change)
        else:
            print_event_not_found(match)
            return None

    if line:
        built_in_flag = False
        cmd = shlex_split(line)[0]
        for i in built_in_functions:
            if cmd.startswith(i):
                run_built_in_func(line, cmd)
                built_in_flag = True
                break
        if not built_in_flag:
            cmd = find_cmd_path(shlex_split(line)[0])
            if cmd:
                print(line)
                run([cmd] + shlex_split(line)[1:])
            else:
                print("intek-sh$ : {}: command not found".format(line))
        history_write(line)
    else:
        print("intek-sh$ : {}: command not found".format(line))


def run_built_in_func(line, func):
    # Run built-in function with subprocess.run

    if func == 'history':
        args = line.split()
        if len(args) == 1:
            print_history()
        elif len(args) == 2:
            print_history(args[1])
        else:
            print_error()


def cmd_history():
    '''
    While working in the Bash shell it is common that you
    to want to repeat a command that you have recently executed
    Bash keeps a history of executed commands in a history file .bash_history
    that you can access by simply typing history

    Bash keeps a history of executed commands in a history file .bash_history
    that you can access by simply typing history

    This will output a list of commands prefixed with an identification number.
    If you only want to see the last N entries in the history, type history N.
    To execute a command from your history, you can use the history expansion
    ! followed by the identification number.

    You can also use !! as a shortcut for executing the last command
    bash: !1450: event not found


    You can also use !! as a shortcut for executing the last command

    bash: !1450: event not found

    !cat: executes that last command to begin with cat. Note that the matching
    string cannot contain any spaces.
    '''

    built_in_functions = ['history']

    line = None

    while line != 'exit':
        line = input("intek-sh$ ")
        if line.startswith('!'):
            exclamation_handle(line, built_in_functions)
        else:
            if len(line.strip()) != 0:
                history_write(line)
            if line.startswith('history'):
                run_built_in_func(line, 'history')
    cmd = None

    while cmd != 'exit':
        cmd = input()
        history_write(cmd)
        if cmd.startswith('history'):
            args = cmd.split()
            if len(args) == 1:
                print_history()
            elif len(args) == 2:
                print_history(args[1])
            else:
                print_error()

    # Create .py_history file

    # Create command function 'history' that access .py_history then output
    # a list of commands were typed prefixed with an identification number

    # Create function that use '!' to execute a command from history
    # Use '!!' to execute the last command

    # !<number> with a number out of history list will output an error

    # !<string=cmd> will execute the last comman begin with 'string'
    # Note: matching string cannot caontain any spaces


def main():
    cmd_history()


if __name__ == '__main__':
   main()
