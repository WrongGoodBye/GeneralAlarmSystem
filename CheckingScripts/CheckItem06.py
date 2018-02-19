import os
import sys
import subprocess
import numpy as np


def get_status():
    status = 0

    if not copy_remote_file_to_local():
        return status

    status = check_logfile()
    return status


def copy_remote_file_to_local():
    remote_usr = 'usrname'
    remote_ip  = 'XXX.XXX.XXX.XXX'
    remote_orginal_filepath = '/XXX/XXX/XXX/XXX.log'
    local_copy_filepath     = './LocalFilename.log'
    ssh_key = '~/.ssh/id_rsa' # you have to set RSA-key for ssh-connection without passwd


    remote_file = remote_usr + '@' + remote_ip + ':' + remote_orginal_filepath
    cmd = ['scp', '-i', ssh_key,
           '-p', remote_file, local_copy_filepath]
    subprocess.run(cmd)
    return True

def check_logfile():
    local_copy_filepath = './LocalFilename.log'
    fin = open(local_copy_filepath, 'r')
    """ read log-file and check working status, unixtime, and etc... """
    failed_case=True
    failed_case=False
    fin.close()

    if failed_case:
        return 2
    else:
        return 1
