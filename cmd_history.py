#!/usr/bin/env python3
import os
from itertools import islice


def history_write(content):
    # Access and write content to history file (.py_history)

    history_filename = '.py_history'
    history_path = os.path.join(os.path.abspath('.'), history_filename)

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
    print('intek-sh$: history: too many arguments')
    exit(1)


def cmd_history():
    '''
    While working in the Bash shell it is common that you
    to want to repeat a command that you have recently executed

    Bash keeps a history of executed commands in a history file .bash_history
    that you can access by simply typing history

    This will output a list of commands prefixed with an identification number.
    If you only want to see the last N entries in the history, type history N.
    To execute a command from your history, you can use the history expansion
    ! followed by the identification number.

    You can also use !! as a shortcut for executing the last command

    bash: !1450: event not found

    !cat: executes that last command to begin with cat. Note that the matching
    string cannot contain any spaces.
    '''

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
