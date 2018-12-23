import os
try:
    pid=os.fork()
except OSError:
    print('not works')
if pid==0:
    print(os.getpid())
