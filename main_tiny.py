
"""
* This is an Auto Item Checking Script, like as the AutoAlarmSystem of
 KamLAND experiment (http://www.awa.tohoku.ac.jp/kamland/)
* Developed with python3.6 as anaconda3(https://www.anaconda.com)
 on macOS(10.13.3)
* This provides a just sample code for general alarm interface
* You have to prepare the checking programs for your purpose
* Written by S.Obara (obara.syuhei.astroparticle@gmail.com)
* First updated on Feburary 19th, 2018
"""

import os
import sys
import tkinter
from tkinter import Tk, ttk
import datetime
import subprocess

import AlertScripts.Mail

import CheckingScripts.CheckItem01  # Set your dir and script name
import CheckingScripts.CheckItem02


CHECK_INTERVAL = 60  # [sec]


class TTinyAlarmSystemApplication(object):
    """oooooooooooooooooooooooooooooooooooooooooooooooooooooo"""
    """oooOOO000 [ Main Body Class of AlarmSystem ] 000OOOooo"""
    """oooooooooooooooooooooooooooooooooooooooooooooooooooooo"""
    
    def __init__(self):

        self.from_address = 'XXX@XXX.ac.jp'  # <-- Mail Sender Address
        self.MailApp = AlertScripts.Mail.TMailTransporter()
        
        self.root = tkinter.Tk()  # Declare constructor of GUI application 
        self.root.title('TinyAlarmSystem(Sample)')

        self.build_gui()  # Build GUI, defined in this class

        self.running = True  # Running flag
        self.timerCounter = int(CHECK_INTERVAL)  # Count-down timer

        self.on_start_up()  # Start
        
        self.root.mainloop()  # Application drawn

        
    def build_gui(self):
        """-----[ Setup GUI mother window ]-----"""
        self.motherFrame = ttk.Frame(self.root, relief=tkinter.FLAT)


        """-----[ Define Colors ]-----"""
        self.COLOR_OK       = '#008000'
        self.COLOR_BAD      = '#ff0000'
        self.COLOR_UPDATING = '#ffff00'


        """-----[ Define Count-down timer & Date display ]-----"""
        self.timerFrame = ttk.Frame(self.motherFrame, relief=tkinter.FLAT)
        self.timerFrame.clockEcho   = tkinter.StringVar()
        self.timerFrame.counterEcho = tkinter.StringVar()
        self.timerFrame.clockLabel   = tkinter.Label(self.timerFrame, textvariable=self.timerFrame.clockEcho,   relief=tkinter.SUNKEN,  width=20)
        self.timerFrame.counterLabel = tkinter.Label(self.timerFrame, textvariable=self.timerFrame.counterEcho, relief=tkinter.SUNKEN,  width=6)
        d    = datetime.datetime.today()
        date = d.strftime('%Y-%m-%d %H:%M:%S')
        self.timerFrame.clockEcho  .set('{}'.format(date))
        self.timerFrame.counterEcho.set(str(CHECK_INTERVAL))
        self.timerFrame.clockLabel  .grid(row=1, column=0, columnspan=6, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.timerFrame.counterLabel.grid(row=1, column=7, columnspan=3, padx=5, pady=2, sticky=tkinter.W+tkinter.E)


        """-----[ Buttons: Update, Quit, and Stop/Start ]-----"""
        """
        The configures of Buttons will not be changed during the system running.
        Therefore, button-related objects are not global (do not need 'self').
        """
        buttonFrame = ttk.Frame(self.motherFrame, relief=tkinter.FLAT)
        buttonFrame.updateButton    = ttk.Button(buttonFrame, text='Update', command=self.update)
        buttonFrame.quitButton      = ttk.Button(buttonFrame, text='Quit',   command=self.quit)
        buttonFrame.stopstartButton = ttk.Button(buttonFrame, text='Stop/Start',   command=self.stopstart)
        buttonFrame.updateButton   .grid(row=0, column=0, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        buttonFrame.quitButton     .grid(row=0, column=1, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        buttonFrame.stopstartButton.grid(row=0, column=2, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)


        
        """-----[  Status, ShiftInfo ]-----"""
        self.statusFrame = ttk.Frame(self.motherFrame)
        self.statusFrame.CheckTarget01StatusLabel = tkinter.Label(self.statusFrame, text='Check01', bg=self.COLOR_UPDATING)
        self.statusFrame.CheckTarget02StatusLabel = tkinter.Label(self.statusFrame, text='Check02', bg=self.COLOR_UPDATING)
        self.statusFrame.CheckTarget01StatusLabel.pack()
        self.statusFrame.CheckTarget02StatusLabel.pack()
               
        
        """[ShiftInfo page]"""
        self.shifterFrame = ttk.Frame(self.motherFrame, relief=tkinter.FLAT)
        self.shifterFrame.titleLabel = ttk.Label(self.shifterFrame, text='Shifter')
        self.shifterFrame.shiftnameEntry = tkinter.Entry(self.shifterFrame)
        self.shifterFrame.shiftmailEntry = tkinter.Entry(self.shifterFrame)

        self.shifterFrame.mailButton = ttk.Button(self.shifterFrame, text='TestMail', command=self.test_mail)
        
        self.shifterFrame.titleLabel    .grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.shifterFrame.shiftnameEntry.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.shifterFrame.shiftmailEntry.grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.shifterFrame.mailButton    .grid(row=2, column=2,               padx=5, pady=2, sticky=tkinter.W+tkinter.E)



        """-----[ All widgets set place ]-----"""
        self.timerFrame.grid(row=0)
        buttonFrame.grid(row=1)
        self.statusFrame.grid(row=2)
        self.shifterFrame.grid(row=3)

        self.motherFrame.pack()




        

    """oooOOO[ Internal Functions ]OOOooo"""
    def system_print(self, print_text):
        print('# SYSTEM({0}): {1}'.format((datetime.datetime.today()).strftime('%Y-%m-%d %H:%M:%S'), print_text))
        return True

    
    def warning_print(self, print_text):
        print('# WARNING:({0}): {1}'.format((datetime.datetime.today()).strftime('%Y-%m-%d %H:%M:%S'), print_text))
        return True
    
        
    def on_start_up(self):    
        self.system_print('start')
        self.count_down_every_1sec() # Start count down loop
        return True

    
    def on_shut_down(self):
        self.system_print('shutdown')
        sys.exit()


    def count_down_every_1sec(self):

        if self.running:
            ##--[ Loop every 1000msec & reflesh window ]--##
            #[timer]
            if self.timerCounter==0:
                self.timerFrame.counterEcho.set('Update')
            elif self.timerCounter < 0:
                self.timerFrame.counterEcho.set('Update')
                self.update_every_interval()
            else :
                self.timerFrame.counterEcho.set('{0:02d}'.format(self.timerCounter))

            d = datetime.datetime.today()
            date = d.strftime('%Y-%m-%d %H:%M:%S')
            self.timerFrame.clockEcho.set('{}'.format(date))
            self.timerCounter = self.timerCounter - 1
            self.root.after(1000, self.count_down_every_1sec)

        else:
            ##--[ count down timer stopped case ]--##
            d = datetime.datetime.today()
            date = d.strftime('%Y-%m-%d %H:%M:%S')
            self.timerFrame.clockEcho.set('{}'.format(date))
            self.root.after(1000, self.count_down_every_1sec)

        return True



    def update_every_interval(self):
        """ here, executes check commands and gives each status """
        """ interval time length can be set by yourself as GlobalInvariable of CHECK_INTERVAL. """
        """ you can execute by system_call function or by hard-coding """

        status_of_check_item01 = 0
        status_of_check_item02 = 0

        """
        status level definition
        0 --> default: updating
        1 --> good
        2 --> bad
        3 --> disable
        """
        colorOfStatus = [self.COLOR_UPDATING, self.COLOR_OK, self.COLOR_BAD, self.COLOR_DISABLE]


        #[check target 01]
        status_of_check_item01 = CheckingScripts.CheckItem01.get_status()
        self.statusFrame.CheckTarget01StatusLabel.configure(bg=colorOfStatus[status_of_check_item01])
        if status_of_check_item01 == 2:
            self.send_an_email('CheckItem01')


        #[check target 02]
        status_of_check_item02 = CheckingScripts.CheckItem02.get_status()
        self.statusFrame.CheckTarget02StatusLabel.configure(bg=colorOfStatus[status_of_check_item02])
        if status_of_check_item02 == 2:
            self.send_an_email('CheckItem02')


        #reset count down timer
        self.timerCounter = int(CHECK_INTERVAL)

        return True


    def send_an_email(self, error_item_name):

        to_address   = str(self.shifterFrame.shiftmailEntry.get())
        from_address = self.from_address
        subject      = '=== {} ==='.format(error_item_name)
        mail_message = 'Abnormal value is detected !!\n by GeneralAlarmSystem\n'        
        if to_address == None:
            sys.stderr.write('# ERROR: to address is not set\n')
            sys.exit()
            return False

        self.MailApp.send(to_address, from_address, subject, mail_message)    
        self.system_print('mail to {0} === {1} ==='.format(to_address, error_item_name))
        return True

    
    
    
    """-----[ Button Functions ]-----"""
    def update(self):
        self.update_every_interval()
        return True

    def quit(self):
        self.running=False
        self.on_shut_down()

    def stopstart(self):
        if self.running==True:
            self.running=False
        else:
            self.running=True
        return

    def test_mail(self):
        self.system_print('test_mail')
        self.send_an_email('Test')
        return  True



##################################################################
##################################################################

if __name__ == '__main__':
    
    root = TTinyAlarmSystemApplication()
    sys.exit()
