
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
import numpy as np
import tkinter
from tkinter import Tk, ttk
from tkinter import messagebox
import datetime
import subprocess
import argparse

import AlertScripts.Mail

import CheckingScripts.CheckItem01  # Set your dir and script name
import CheckingScripts.CheckItem02
import CheckingScripts.CheckItem03
import CheckingScripts.CheckItem04
import CheckingScripts.CheckItem05
import CheckingScripts.CheckItem06


WORKING_BASE_DIR = os.getcwd()  # or set working dir
CHECK_INTERVAL = 60  # [sec]
DEFAULT_USR  = 'shifter name'  # Set default shifter name
DEFAULT_MAIL = 'shift@address.co.jp'  # Set default shifter address


class TGeneralAlarmSystemApplication(object):
    """oooooooooooooooooooooooooooooooooooooooooooooooooooooo"""
    """oooOOO000 [ Main Body Class of AlarmSystem ] 000OOOooo"""
    """oooooooooooooooooooooooooooooooooooooooooooooooooooooo"""
    
    def __init__(self, mode='normal'):

        self.mode = mode
        self.from_address = 'XXX@XXX.ac.jp'  # Set mail sender addrss
        self.MailApp = AlertScripts.Mail.TMailTransporter()
        
        self.root = tkinter.Tk()  # Declare constructor of GUI application 
        self.root.title('GeneralAlarmSystem(Sample)')

        self.build_gui()  # Build GUI, defined in this class

        self.running = True  # Running flag
        self.timerCounter = int(CHECK_INTERVAL)  # Count-down timer

        self.on_start_up()  # Start
        
        self.root.mainloop()  # Application drawn
        

        
        
    def build_gui(self):
        """-----[ Setup GUI mother window ]-----"""
        self.motherFrame = ttk.Frame(self.root, relief=tkinter.FLAT)


        """-----[ Define Colors ]-----"""
        self.COLOR_BLACK    = '#000000'
        self.COLOR_WHITE    = '#ffffff'
        self.COLOR_OK       = '#008000'
        self.COLOR_BAD      = '#ff0000'
        self.COLOR_LOWLEVEL = '#ffa500'
        self.COLOR_UPDATING = '#ffff00'
        self.COLOR_DISABLE  = '#a9a9a9'
        self.COLOR_GRAY     = '#bfbfbf'

        """-----[ Define Config filename ]-----"""
        self.CONFIG_FILENAME = '{}/config.txt'.format(WORKING_BASE_DIR)
        

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


        """-----[ NoteBook Frame: Status, ShiftInfo, and Config Pages ]-----"""
        self.noteFrame = ttk.Frame(self.motherFrame, relief=tkinter.FLAT)
        self.noteFrame.notebook  = ttk.Notebook(self.noteFrame)
        self.noteFrame.notebook.statusPage    = ttk.Frame(self.noteFrame.notebook)
        self.noteFrame.notebook.shiftinfoPage = ttk.Frame(self.noteFrame.notebook)
        self.noteFrame.notebook.configPage    = ttk.Frame(self.noteFrame.notebook)
        self.noteFrame.notebook.add(self.noteFrame.notebook.statusPage,    text='Status',    sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.add(self.noteFrame.notebook.shiftinfoPage, text='ShiftInfo', sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.add(self.noteFrame.notebook.configPage,    text='Config',    sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.pack(fill=tkinter.BOTH)

        """[Status page]"""
        self.noteFrame.notebook.statusPage.monitoringstatusLabel = ttk.Label(self.noteFrame.notebook.statusPage, text='Monitoring Status', anchor='w')

        
        LABELWIDTH = 9
        self.noteFrame.notebook.statusPage.statusColorFrame = ttk.Frame(self.noteFrame.notebook.statusPage)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget01StatusLabel = tkinter.Label(self.noteFrame.notebook.statusPage.statusColorFrame, text='Check01', width=LABELWIDTH, bg=self.COLOR_UPDATING)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget02StatusLabel = tkinter.Label(self.noteFrame.notebook.statusPage.statusColorFrame, text='Check02', width=LABELWIDTH, bg=self.COLOR_UPDATING)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget03StatusLabel = tkinter.Label(self.noteFrame.notebook.statusPage.statusColorFrame, text='Check03', width=LABELWIDTH, bg=self.COLOR_UPDATING)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget04StatusLabel = tkinter.Label(self.noteFrame.notebook.statusPage.statusColorFrame, text='Check04', width=LABELWIDTH, bg=self.COLOR_UPDATING)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget05StatusLabel = tkinter.Label(self.noteFrame.notebook.statusPage.statusColorFrame, text='Check05', width=LABELWIDTH*2, bg=self.COLOR_UPDATING)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget06StatusLabel = tkinter.Label(self.noteFrame.notebook.statusPage.statusColorFrame, text='Check06', width=LABELWIDTH*3, bg=self.COLOR_UPDATING)


        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget01StatusLabel.grid(row=0, column=0, columnspan=1, padx=3, pady=3, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget02StatusLabel.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget03StatusLabel.grid(row=0, column=2, columnspan=1, padx=3, pady=3, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget04StatusLabel.grid(row=1, column=0, columnspan=1, padx=3, pady=3, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget05StatusLabel.grid(row=1, column=1, columnspan=2, padx=3, pady=3, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget06StatusLabel.grid(row=2, column=0, columnspan=3, padx=3, pady=3, sticky=tkinter.W+tkinter.E)

        
        self.noteFrame.notebook.statusPage.legendFrame = ttk.Frame(self.noteFrame.notebook.statusPage, relief=tkinter.FLAT)
        self.noteFrame.notebook.statusPage.legendFrame.legendLabel         = ttk.Label(self.noteFrame.notebook.statusPage.legendFrame, text='Legends:')
        self.noteFrame.notebook.statusPage.legendFrame.legendOkLabel       = tkinter.Label(self.noteFrame.notebook.statusPage.legendFrame, text='OK',       bg=self.COLOR_OK)
        self.noteFrame.notebook.statusPage.legendFrame.legendBadLabel      = tkinter.Label(self.noteFrame.notebook.statusPage.legendFrame, text='BAD',      bg=self.COLOR_BAD)
        self.noteFrame.notebook.statusPage.legendFrame.legendLowLevelLabel = tkinter.Label(self.noteFrame.notebook.statusPage.legendFrame, text='Warning',  bg=self.COLOR_LOWLEVEL)
        self.noteFrame.notebook.statusPage.legendFrame.legendUpdateLabel   = tkinter.Label(self.noteFrame.notebook.statusPage.legendFrame, text='Updating', bg=self.COLOR_UPDATING)
        self.noteFrame.notebook.statusPage.legendFrame.legendDisableLabel  = tkinter.Label(self.noteFrame.notebook.statusPage.legendFrame, text='Disable',  bg=self.COLOR_DISABLE)
        self.noteFrame.notebook.statusPage.legendFrame.legendNALabel       = tkinter.Label(self.noteFrame.notebook.statusPage.legendFrame, text='N/A',      bg=self.COLOR_WHITE)

        self.noteFrame.notebook.statusPage.legendFrame.legendLabel        .grid(row=0, column=0, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.legendFrame.legendOkLabel      .grid(row=0, column=1, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.legendFrame.legendBadLabel     .grid(row=0, column=2, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.legendFrame.legendLowLevelLabel.grid(row=0, column=3, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.legendFrame.legendUpdateLabel  .grid(row=1, column=1, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.legendFrame.legendDisableLabel .grid(row=1, column=2, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.legendFrame.legendNALabel      .grid(row=1, column=3, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)

        self.noteFrame.notebook.statusPage.monitoringstatusLabel.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.statusColorFrame     .grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.statusPage.legendFrame          .grid(row=2, column=0, sticky=tkinter.W+tkinter.E)

        """[ShiftInfo page]"""
        self.noteFrame.notebook.shiftinfoPage.shifterFrame = ttk.Frame(self.noteFrame.notebook.shiftinfoPage, relief=tkinter.FLAT)
        self.noteFrame.notebook.shiftinfoPage.shifterFrame .grid(row=0, column=0, sticky=tkinter.W+tkinter.E)

        self.noteFrame.notebook.shiftinfoPage.shifterFrame.titleLabel = ttk.Label(self.noteFrame.notebook.shiftinfoPage.shifterFrame, text='Shifter')

        self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftnameEntry = tkinter.Entry(self.noteFrame.notebook.shiftinfoPage.shifterFrame)

        self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftmailEntry = tkinter.Entry(self.noteFrame.notebook.shiftinfoPage.shifterFrame)

        self.noteFrame.notebook.shiftinfoPage.shifterFrame.mailButton = ttk.Button(self.noteFrame.notebook.shiftinfoPage.shifterFrame, text='TestMail', command=self.test_mail)

        self.noteFrame.notebook.shiftinfoPage.shifterFrame.titleLabel    .grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftnameEntry.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftmailEntry.grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.shiftinfoPage.shifterFrame.mailButton    .grid(row=2, column=2,               padx=5, pady=2, sticky=tkinter.W+tkinter.E)



        """[Config page]"""
        self.noteFrame.notebook.configPage.configFrame = ttk.Frame(self.noteFrame.notebook.configPage, relief=tkinter.FLAT)
        self.noteFrame.notebook.configPage.configFrame.grid(row=0, column=0, sticky=tkinter.W+tkinter.E)

        self.is_check_target01 = tkinter.BooleanVar()
        self.is_check_target02 = tkinter.BooleanVar()
        self.is_check_target03 = tkinter.BooleanVar()
        self.is_check_target04 = tkinter.BooleanVar()
        self.is_check_target05 = tkinter.BooleanVar()
        self.is_check_target06 = tkinter.BooleanVar()
        self.is_check_target01.set(True)  # default value set in self.load_last_config()
        self.is_check_target02.set(True)
        self.is_check_target03.set(True)
        self.is_check_target04.set(True)
        self.is_check_target05.set(True)
        self.is_check_target06.set(True)

        
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget01 = ttk.Checkbutton(self.noteFrame.notebook.configPage.configFrame, text='Check01', variable=self.is_check_target01)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget02 = ttk.Checkbutton(self.noteFrame.notebook.configPage.configFrame, text='Check02', variable=self.is_check_target02)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget03 = ttk.Checkbutton(self.noteFrame.notebook.configPage.configFrame, text='Check03', variable=self.is_check_target03)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget04 = ttk.Checkbutton(self.noteFrame.notebook.configPage.configFrame, text='Check04', variable=self.is_check_target04)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget05 = ttk.Checkbutton(self.noteFrame.notebook.configPage.configFrame, text='Check05', variable=self.is_check_target05)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget06 = ttk.Checkbutton(self.noteFrame.notebook.configPage.configFrame, text='Check06', variable=self.is_check_target06)

        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget01.grid(row=0, column=0, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget02.grid(row=0, column=1, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget03.grid(row=0, column=2, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget04.grid(row=1, column=0, columnspan=1, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget05.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.noteFrame.notebook.configPage.configFrame.checkButtonCheckTarget06.grid(row=2, column=0, columnspan=3, padx=5, pady=2, sticky=tkinter.W+tkinter.E)



        """-----[ All widgets set place ]-----"""
        self.timerFrame.pack()
        buttonFrame    .pack()
        self.noteFrame .pack()
        self.motherFrame.pack()




        

    """oooOOO[ Internal Functions ]OOOooo"""
    def system_print(self, print_text):
        print('# SYSTEM({0}): {1}'.format((datetime.datetime.today()).strftime('%Y-%m-%d %H:%M:%S'), print_text))
        return True

    
    def warning_print(self, print_text):
        print('# WARNING:({0}): {1}'.format((datetime.datetime.today()).strftime('%Y-%m-%d %H:%M:%S'), print_text))
        return True
    
        
    def on_start_up(self):    
        if self.mode=='debug':
            # Confirm to continue with debug-mode
            if messagebox.askyesno('Confirmation','Continue with Debug-mode?'):
                self.system_print('start with debug-mode')
            else:
                self.on_shut_down()
                
        else:
            self.system_print('start with normal')

        self.load_last_config()  # Load last configure setup
        self.count_down_every_1sec()  # Start count down loop
        return True

    
    def on_shut_down(self):
        if not self.mode=='debug':
            self.save_last_config()
            
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
            self.save_last_config()
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
        status_of_check_item03 = 0
        status_of_check_item04 = 0
        status_of_check_item05 = 0
        status_of_check_item06 = 0
        """
        status level definition
        0 --> default: updating
        1 --> good
        2 --> bad
        3 --> disable
        4 --> warning
        """
        colorOfStatus = [self.COLOR_UPDATING, self.COLOR_OK, self.COLOR_BAD, self.COLOR_DISABLE, self.COLOR_LOWLEVEL]

        #[check target 01]
        if self.is_check_target01.get() == True:
            status_of_check_item01 = CheckingScripts.CheckItem01.get_status()
        else:
            status_of_check_item01 = 3
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget01StatusLabel.configure(bg=colorOfStatus[status_of_check_item01])
        if status_of_check_item01 == 2 or status_of_check_item01 == 4:
            self.send_an_email('CheckItem01')


        #[check target 02]
        if self.is_check_target02.get() == True:
            status_of_check_item02 = CheckingScripts.CheckItem02.get_status()
        else:
            status_of_check_item02 = 3
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget02StatusLabel.configure(bg=colorOfStatus[status_of_check_item02])
        if status_of_check_item02 == 2 or status_of_check_item02 == 4:
            self.send_an_email('CheckItem02')


        #[check target 03]
        if self.is_check_target03.get() == True:
            status_of_check_item03 = CheckingScripts.CheckItem03.get_status()
        else:
            status_of_check_item03 = 3
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget03StatusLabel.configure(bg=colorOfStatus[status_of_check_item03])
        if status_of_check_item03 == 2 or status_of_check_item03 == 4:
            self.send_an_email('CheckItem03')


        #[check target 04]
        if self.is_check_target04.get() == True:
            status_of_check_item04 = CheckingScripts.CheckItem04.get_status()
        else:
            status_of_check_item04 = 3
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget04StatusLabel.configure(bg=colorOfStatus[status_of_check_item04])
        if status_of_check_item04 == 2 or status_of_check_item04 == 4:
            self.send_an_email('CheckItem04')


        #[check target 05]
        if self.is_check_target05.get() == True:
            status_of_check_item05 = CheckingScripts.CheckItem05.get_status()
        else:
            status_of_check_item05 = 3
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget05StatusLabel.configure(bg=colorOfStatus[status_of_check_item05])
        if status_of_check_item05 == 2 or status_of_check_item05 == 4:
            self.send_an_email('CheckItem05')


        #[check target 06]
        if self.is_check_target06.get() == True:
            status_of_check_item06 = CheckingScripts.CheckItem06.get_status()
        else:
            status_of_check_item06 = 3
        self.noteFrame.notebook.statusPage.statusColorFrame.CheckTarget06StatusLabel.configure(bg=colorOfStatus[status_of_check_item06])
        if status_of_check_item06 == 2 or status_of_check_item06 == 4:
            self.send_an_email('CheckItem06')


        #reset count down timer
        self.timerCounter = int(CHECK_INTERVAL)

        return True


    def send_an_email(self, error_item_name):

        to_address   = str(self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftmailEntry.get())
        from_address = self.from_address
        subject      = '=== {} ==='.format(error_item_name)
        mail_message = 'by GeneralAlarmSystem\n'

        """ address check """
        if to_address == None:
            sys.stderr.write('# ERROR: to address is not set\n')
            sys.exit()
            return False

        """ set message """
        if error_item_name == 'CheckItem01':
            mail_message = 'CheckItem01 alarm means very serious condition. Please contact expert ASAP. XXX-XXX-XXX. \n by GeneralAlarmSystem\n'
        elif error_item_name == 'CheckItem02':
            mail_message = 'Please check HV-supply\n'
        # This "mail_message" can be written as you like for each case!!

        
        if self.mode=='debug':
            # Skip mail transportaion in case of debug
            self.system_print('alert to {0} === {1} === w/o mail-transportation(debug)'.format(to_address, error_item_name))
        else:
            self.MailApp.send(to_address, from_address, subject, mail_message)
            self.system_print('mail to {0} === {1} ==='.format(to_address, error_item_name))
        return True

    
    def save_last_config(self):

        shifter_name = str(self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftnameEntry.get())
        shifter_mail = str(self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftmailEntry.get())
        if shifter_name==None:
            self.warning_print('empty shifter name')
            shifter_name = DEFAULT_USR
        if shifter_mail==None:
            self.warning_print('empty shifter mail address')
            shifter_mail = DEFAULT_MAIL

        boolean_check_target01 = self.is_check_target01.get()
        boolean_check_target02 = self.is_check_target02.get()
        boolean_check_target03 = self.is_check_target03.get()
        boolean_check_target04 = self.is_check_target04.get()
        boolean_check_target05 = self.is_check_target05.get()
        boolean_check_target06 = self.is_check_target06.get()
                    
        fout = open(self.CONFIG_FILENAME, 'w')
        fout.write('{}\n'.format(shifter_name))
        fout.write('{}\n'.format(shifter_mail))
        fout.write('{}\n'.format(boolean_check_target01))
        fout.write('{}\n'.format(boolean_check_target02))
        fout.write('{}\n'.format(boolean_check_target03))
        fout.write('{}\n'.format(boolean_check_target04))
        fout.write('{}\n'.format(boolean_check_target05))
        fout.write('{}\n'.format(boolean_check_target06))
        fout.close()
        
        return True

    
    def load_last_config(self):
        if not os.path.isfile(self.CONFIG_FILENAME):
            self.system_print('failed load last config, set default value')
            return False
        
        fin = open(self.CONFIG_FILENAME, 'r')
        shifter_name = fin.readline()    
        self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftnameEntry.insert(tkinter.END, shifter_name.rstrip())
        shifter_mail = fin.readline()
        self.noteFrame.notebook.shiftinfoPage.shifterFrame.shiftmailEntry.insert(tkinter.END, shifter_mail.strip())

        boolean_check_target01 = fin.readline()
        self.is_check_target01.set(boolean_check_target01.strip())
        boolean_check_target02 = fin.readline()
        self.is_check_target02.set(boolean_check_target02.strip())
        boolean_check_target03 = fin.readline()
        self.is_check_target03.set(boolean_check_target03.strip())
        boolean_check_target04 = fin.readline()
        self.is_check_target04.set(boolean_check_target04.strip())
        boolean_check_target05 = fin.readline()
        self.is_check_target05.set(boolean_check_target05.strip())
        boolean_check_target06 = fin.readline()
        self.is_check_target06.set(boolean_check_target06.strip())
        fin.close()
        self.system_print('load last config from "{}"'.format(self.CONFIG_FILENAME))
        
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
    
    parser = argparse.ArgumentParser(description='Here, you can display messeages when Option -h\n')
    parser.add_argument('-d', '--debug', action='store_const', const=True, default=False, help='set debug-mode=True (default: False)')
    args = parser.parse_args()

    if args.debug:        
        root = TGeneralAlarmSystemApplication('debug')
    else:
        root = TGeneralAlarmSystemApplication()

    sys.exit()
