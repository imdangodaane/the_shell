#!/usr/bin/env python3
import subprocess
import os
import collections
import sys
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - \
%(levelname)s - %(message)s')
logging.disable(logging.DEBUG)


def bin_cd(args):
    '''
    Change current directory to another directory
    cd ~: change to HOME directory
    cd -: change to previous directory
    cd <path>: change to path directory
    '''
    if args:
        arg = args.popleft()
    else:
        arg = ''
    if arg == '-':
        if os.environ['OLDPWD']:
            temp = os.getcwd()
            os.chdir(os.environ['OLDPWD'])
            os.environ['OLDPWD'] = temp
        else:
            print('intek-sh: cd: OLDPWD not set' % arg)
    elif arg and arg != '~':
        if os.path.isdir(arg):
            os.environ['OLDPWD'] = os.getcwd()
            os.chdir(os.path.abspath(arg))
        else:
            print('cd: %s: No such file or directory' % arg)
    else:
        try:
            home = os.environ['HOME']
            os.environ['OLDPWD'] = os.getcwd()
            os.chdir(home)
        except KeyError:
            print('intek-sh: cd: HOME not set')


def bin_printenv(args):
    '''
    Print all environment variables if there're no arguments pass to cmd-line
    Print environment variable if give name
    '''
    _dict = dict(os.environ)
    if args:
        for arg in args:
            if arg in _dict.keys():
                print(_dict[arg])
            else:
                pass
    else:
        for keys, values in _dict.items():
            print(keys + '=' + values)


def bin_export(args):
    '''
    Set an environment variable with value
    '''
    for arg in args:
        if arg.count('=') < 1:
            left = arg
            right = ''
        elif arg.count('=') == 1:
            # if len(arg.split('=')) == 2:
            left = arg.split('=')[0]
            right = arg.split('=')[1]
            logging.debug('Left = %s' % left)
            logging.debug('Right = %s' % right)
        elif arg.count('=') > 1:
            left = arg[:arg.find('=')]
            right = arg[arg.find('=') + 1:]
        os.environ[left] = right
        logging.debug('os.environ[%s] = %s' % (left, right))


def bin_unset(args):
    '''
    Remove an environment variable
    '''
    if args:
        for arg in args:
            try:
                del os.environ[arg]
            except KeyError:
                pass


def bin_exit(args):
    '''
    Exit program with code, print solid string if input code was string
    '''
    code = 0
    if args:
        try:
            code = int(args[0])
        except ValueError:
            sys.exit('exit\nintek-sh: exit:')
    print('exit')
    sys.exit(code)


def main():
    '''
    Main function to handle input from user
    '''
    while True:
        # Handle EOFError when input End Of File.
        try:
            line = input('intek-sh$ ')
        except EOFError:
            sys.exit(1)
        # Split arguments for easy handling.
        args = collections.deque(line.split())
        if args:
            cmd = args.popleft()
            # cd build-in function
            if cmd == 'cd':
                bin_cd(args)
            # printenv build-in function
            elif cmd == 'printenv':
                bin_printenv(args)
            # export build-in function
            elif cmd == 'export':
                bin_export(args)
            # unset build-in function
            elif cmd == 'unset':
                bin_unset(args)
            # exit build-in function
            elif cmd == 'exit':
                bin_exit(args)
            # External binaries handling
            else:
                found_flag = False
                head_cmd = cmd
                try:
                    if './' == cmd[0:2]:
                        path = os.getcwd()
                        cmd = cmd.split('./')[1]
                    else:
                        path = os.environ['PATH']
                    logging.debug('Path = %s' % path)
                except KeyError:
                    print('intek-sh: wc: command not found')
                    continue
                if path:
                    for dir in path.split(':'):
                        try:
                            cmd_list = os.listdir(dir)
                        except FileNotFoundError:
                            continue
                        logging.debug('Command list: %s' % cmd_list)
                        if cmd in cmd_list:
                            found_flag = True
                            if os.access(os.path.join(dir, cmd), os.X_OK):
                                args.appendleft(os.path.join(dir, cmd))
                                logging.debug('args = %s' % args)
                                subprocess.run(args)
                                break
                            else:
                                print('intek-sh: %s: Permission denied'
                                      % head_cmd)
                                break
                    if not found_flag:
                        print('intek-sh: %s: command not found' % head_cmd)


if __name__ == '__main__':
    main()
