import subprocess
import sys


def package(filename: str):
    command = [
        'nuitka',
        '--standalone',
        '--enable-plugin=pyqt5',
        filename
        ]
    p = subprocess.Popen(command, shell=True)
    p.wait()


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 1:
        print("用法：Python NuitkaPackaging.py filename")
    else:
        package(argv[1])
