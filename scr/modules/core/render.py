import sys
import os


def get_key():
    if os.name == 'nt':
        return get_windows_key()
    else:
        return get_linux_key()


def get_windows_key():
    import msvcrt
    return msvcrt.getch().decode('utf-8')


def get_linux_key():
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key



