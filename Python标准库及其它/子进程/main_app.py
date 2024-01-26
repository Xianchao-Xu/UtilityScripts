# coding: utf-8
# author: xuxc
from subprocess import Popen, PIPE

with Popen(['python', 'sub_app.py'], stdin=PIPE) as p:
    p.stdin.write(b'3\n')
    p.stdin.write(b'4\n')
