# coding: utf-8
# author: xuxc
import argparse
import os
from subprocess import Popen, PIPE


def run_peps(exe_path, filename):
    ext_list = ['.prd', '.pre', '.pri', '.prl', '.prr']
    with Popen([exe_path], stdin=PIPE) as p:
        # Is there a COMMAND file? (Y/N) :
        p.stdin.write(b'N\n')
        # Enter name of free format input file :
        p.stdin.write(bytes(filename, 'utf-8') + b'.fre\n')

        restart = False
        for ext in ext_list:
            name = filename + ext
            if os.path.exists(name):
                restart = True
                break

        # Overwrite existing report files for this problem? (Y=yes):
        if restart:
            p.stdin.write(b'Y\n')

        # Is there an input restart file? (Y/N=default) :
        p.stdin.write(b'\n')
        # Enter name of output restart file
        p.stdin.write(b'\n')
        # Enter number of lines-per-page (default=50)  :
        p.stdin.write(b'\n')
        # Enter name of work path
        p.stdin.write(b'\n')
        # work files will be written in local directory is this ok? (Y=default/N=no,Q=quit) :
        p.stdin.write(b'\n')
        # Execute PIPESTRESS? (Y=yes) :
        p.stdin.write(b'N\n')


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    # peps的可执行文件为：PSEXE_Demo.EXE
    arg_parser.add_argument('exe')
    # 输入脚本不能带后缀
    arg_parser.add_argument('filename')
    given_args = arg_parser.parse_args()
    exe = given_args.exe
    peps_file = given_args.filename
    run_peps(exe, peps_file)
