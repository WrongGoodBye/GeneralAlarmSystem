"""
* This is a wrapper for mail-transportation via /usr/sbin/sendmail command
"""

import os
import sys
import subprocess

class TMailTransporter(object):
    def __init__(self):
        self.send_mail_command = '/usr/sbin/sendmail'  # <-- set usr's path
        if not os.path.isfile(self.send_mail_command):
            sys.stderr.write('# ERROR: not found sendmail command "{}"\n'.format(self.send_mail_command))
            sys.exit()
            
        self.to_address   = ''
        self.from_address = ''
        

    def send(self, to_address, from_address, subject, message):
        self.to_address   = to_address
        self.from_address = from_address
        
        temporary_mail_body_filename = './tmp_mail_body.txt'
        fout = open(temporary_mail_body_filename, 'w')
        fout.write('From: {}\n'.format(from_address))
        fout.write('To: {}\n'.format(to_address))
        fout.write('Subject: {}\n'.format(subject))
        fout.write('Content-Transfer-Encoding: 7bit\n')
        fout.write('Content-Type: text/plain\n')
        fout.write('\n')
        fout.write('{}\n'.format(message))
        fout.write('.\n')
        fout.close()

        cmd = self.send_mail_command + ' -i -f ' + self.from_address + ' -t ' + self.to_address + ' < ' + temporary_mail_body_filename
        #print(cmd)
        prc = subprocess.run(cmd, shell=True)
        os.remove(temporary_mail_body_filename)        
        return True

    def quit_app(self):
        sys.exit()
        
if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs)<5:
        sys.stderr.write('# Usage: {} [ToAddress] [FromAddress] [Subject] [Message]\n'.format(__file__))
        sys.exit()

    to_ad   = argvs[1]
    from_ad = argvs[2]
    subj = argvs[3]
    msg = ''
    for i in range(4, len(argvs)):
        msg += argvs[i] + ' '
        
    app = TMailTransporter()
    app.send(to_ad, from_ad, subj, msg)
    sys.exit()
        
