
"""
* This provides a sample code for checking logger
* Assuming its format is ; [unixtime] [pmt gain value]\n
* Firstly, copy the log-file from remote-PC
* In case of that scp command spent for too long time, kill its process
* Secondary, confirm its update timing and data range comparing with setting thresholds
* Return status value of ; 1 for good status case, 2 for bad status case, and 4 for update failure case.
"""

import os
import sys
import subprocess
import datetime
import time

class TEasyLogChecker(object):
    """ Sample Class for Checking DAQ Log """
    def __init__(self):
        
        ### Usr Setting Parametes [ssh connection] ###
        self.remote_usr = 'pmt_gain_monitor'
        self.remote_ip  = 'XXX.XXX.XXX.XXX'
        self.remote_orginal_filepath = '/home/pmt/gain/value.log'
        self.local_copy_filepath     = './LocalFilename.log'
        self.ssh_key = '~/.ssh/id_rsa.pmt_monitor_pc'
        # you have to set RSA-key for ssh-connection without passwd
        self.max_time_for_wainting_ssh_connection = 0.5  # [sec]
        self.waiting_time_bin = 0.05  # [sec]

        ### Usr Setting Parametes [logger analysis] ###
        self.LowerThreshold = 0.7  # [p.e.]
        self.UpperThreshold = 3    # [p.e.]
        self.LoggerOutputInterval = 180  # [sec]

        
    def get_status(self):
        if not self.copy_remote_file_to_local():
            return 4
        else:
            return self.check_logfile()



    def copy_remote_file_to_local(self):
        remote_file = self.remote_usr + '@' + self.remote_ip + ':' + self.remote_orginal_filepath
        cmd = 'scp -i ' + self.ssh_key + ' -p ' + remote_file + ' ' + self.local_copy_filepath
        prc = subprocess.Popen(cmd, shell=True)
        cnt = 0
        while prc.poll()==None :
            if cnt*self.waiting_time_bin >= self.max_time_for_wainting_ssh_connection:
                """ In case of that ssh-copy spent too long time """
                prc.terminate()
                return False
            time.sleep(self.waiting_time_bin)
            cnt = cnt + 1
            
        return True


    def check_logfile(self):

        current_unixtime = int(datetime.datetime.now().strftime('%s'))

        fin = open(self.local_copy_filepath, 'r')
        lines = fin.readlines()
        fin.close()
        
        """ assuming the logger file format set as ; [ut] [data]\n """
        last_line = lines[-1]
        items = last_line.split()
        if not len(items)==2:
            """ In case of wrong format of logger file """
            return 4
        
        ut = int(items[0])
        pmt_gain_value = float(items[1])

        if ut > current_unixtime:
            """ In case of that remotePC lives in future """
            return 2
        
        if current_unixtime - ut > self.LoggerOutputInterval :
            """ In case of that data is not updated """
            return 2

        if pmt_gain_value<self.LowerThreshold or pmt_gain_value>self.UpperThreshold:
            """ In case of that data exceeds setting thresholds """
            return 2

        """ In case of that no anomary is found """
        return 1
            
