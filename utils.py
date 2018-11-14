import os
from subprocess import DEVNULL, STDOUT, call


def ping(ip):
    # If windows
    if os.name == 'nt':
        command = ['ping', '-n', '1', '-w', '10', ip]
    # If Linux
    else:
        command = ['ping', '-c', '1', '-W', '10', ip]

    return call(command, stdout=DEVNULL, stderr=STDOUT) == 0
