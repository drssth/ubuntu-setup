import os, os.path
import subprocess


def load_content(fn):
    ls = []
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            r = f.read()
            ls = r.split()
    return ls
    


def run_command(ls):
    print('==> RUN CMD', ' '.join(ls))
    process = subprocess.Popen(ls,
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))
    return stdout.decode('utf-8').strip()
