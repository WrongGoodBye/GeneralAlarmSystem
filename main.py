
"""
* This is an Auto Item Checking Script, like as the AutoAlarmSystem of
 KamLAND experiment (http://www.awa.tohoku.ac.jp/kamland/)
* Developed with python3.6 as anaconda3(https://www.anaconda.com)
 on macOS(10.13.3)
* This provides a just sample code for general alarm interface
* You have to prepare the checking programs for your purpose
* Written by S.Obara (obara.syuhei.astroparticle@gmail.com)
"""

import os
import sys
import tkinter
from tkinter import Tk, ttk
import datetime
import subprocess
import argparse

import AlertScripts.Mail  # Mail transponder script

import CheckingScripts.CheckItem01  # Set your dir and script name
import CheckingScripts.CheckItem02
import CheckingScripts.CheckItem03
import CheckingScripts.CheckItem04
import CheckingScripts.CheckItem05
#import CheckingScripts.CheckItem06

#import CheckingScripts.CheckSample001  # One of the realistic sample


class TGeneralAlarmSystemApplication(object):
    """oooooooooooooooooooooooooooooooooooooooooooooooooooooo"""
    """oooOOO000 [ Main Body Class of AlarmSystem ] 000OOOooo"""
    """oooooooooooooooooooooooooooooooooooooooooooooooooooooo"""

    def __init__(self, mode='normal'):

        """--- USER SETTING: CHECK ITEM NUMBER, NAMES, AND SCRIPTS ---"""
        self.CHECK_INTERVAL = 60  # [sec]
        self.NUBER_OF_CHECK_ITEMS = 5
        self.ItemLabelNames = ['Item01',
                               'Name02',
                               'CheckItem03',
                               'fugafuga',
                               'hogehoge']
        self.ItemScripts = [CheckingScripts.CheckItem01,
                            CheckingScripts.CheckItem02,
                            CheckingScripts.CheckItem03,
                            CheckingScripts.CheckItem04,
                            CheckingScripts.CheckItem05]
        """--------------------------------------------------------"""
        if not len(self.ItemLabelNames) == self.NUBER_OF_CHECK_ITEMS:
            print('# ERROR: set item name')
            sys.exit()
        if not len(self.ItemScripts) == self.NUBER_OF_CHECK_ITEMS:
            print('# ERROR: set script name')
            sys.exit()


        self.from_address = 'XXX@XXX.ac.jp'  # Set mail sender addrss
        self.MailApp = AlertScripts.Mail.TMailTransporter()

        self.root = tkinter.Tk()  # Declare constructor of GUI application
        self.root.title('GeneralAlarmSystem (SampleCode)')

        self.CONFIG_FILENAME = './config.txt' # A file for saving config

        
        """-----[ mode check ]-----"""
        self.mode = mode
        if self.mode == 'debug':
            # confirm to continue with debug-mode
            loop = True
            while loop:
                print('======================================')
                print('== continue with debug mode ? [y/n] ==')
                print('======================================')
                YN = input('>> ')
                if YN == 'y' or YN == 'yes':
                    loop = False
                elif YN == 'n' or YN == 'no':
                    sys.exit()

        elif self.mode == 'clean':
            # clean option case, delete unnecessary files
            delete_file_list = [self.CONFIG_FILENAME]
            for delete_file in delete_file_list:
                self.system_print('delete {}'.format(delete_file))
                os.remove(delete_file)
            sys.exit()

        else:
            # normal mode case
            pass

        self.system_print('start with {} mode'.format(self.mode))


        """-----[ GUI building ]------"""

        """-----[ Setup GUI mother window ]-----"""
        motherFrame = ttk.Frame(self.root, relief=tkinter.FLAT)
        applicationTitleLabel = ttk.Label(motherFrame,
                                          text='SampleApp Ver.X.X')
        applicationTitleLabel.pack(pady=1)

        """-----[ Define Colors ]-----"""
        COLOR_WHITE    = '#ffffff'
        COLOR_OK       = '#008000'
        COLOR_BAD      = '#ff0000'
        COLOR_LOWLEVEL = '#ffa500'
        COLOR_UPDATING = '#ffff00'
        COLOR_DISABLE  = '#a9a9a9'
        self.colorOfStatus = [COLOR_UPDATING,
                              COLOR_OK,
                              COLOR_BAD,
                              COLOR_DISABLE,
                              COLOR_LOWLEVEL]

        """-----[ Define Count-down timer & Date display ]-----"""
        timerFrame = ttk.Frame(motherFrame, relief=tkinter.FLAT)
        self.clockEcho   = tkinter.StringVar()
        self.counterEcho = tkinter.StringVar()
        date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.clockEcho  .set('{}'.format(date))
        self.counterEcho.set(str(self.CHECK_INTERVAL))
        clockLabel   = tkinter.Label(timerFrame,
                                     textvariable=self.clockEcho,
                                     relief=tkinter.SUNKEN, width=20)
        counterLabel = tkinter.Label(timerFrame,
                                     textvariable=self.counterEcho,
                                     relief=tkinter.SUNKEN, width=6)
        clockLabel  .pack(pady=1, side=tkinter.LEFT)
        counterLabel.pack(pady=1, side=tkinter.LEFT)

        """-----[ Buttons: Update, Quit, and Stop/Start ]-----"""
        buttonFrame = ttk.Frame(motherFrame, relief=tkinter.FLAT)
        updateButton    = ttk.Button(buttonFrame,
                                     text='Update',
                                     command=self.update_cmd)
        quitButton      = ttk.Button(buttonFrame,
                                     text='Quit',
                                     command=self.quit_cmd)
        stopstartButton = ttk.Button(buttonFrame,
                                     text='Stop/Start',
                                     command=self.stopstart_cmd)
        updateButton   .pack(pady=1, side=tkinter.LEFT)
        quitButton     .pack(pady=1, side=tkinter.LEFT)
        stopstartButton.pack(pady=1, side=tkinter.LEFT)

        """-----[ NoteBook Frame: Status, ShiftInfo, and Config Pages ]-----"""
        noteFrame = ttk.Frame(motherFrame, relief=tkinter.FLAT)
        notebook = ttk.Notebook(noteFrame)
        statusPage    = ttk.Frame(notebook)
        shiftinfoPage = ttk.Frame(notebook)
        configPage    = ttk.Frame(notebook)
        notebook.add(statusPage,    text='Status')
        notebook.add(shiftinfoPage, text='ShiftInfo')
        notebook.add(configPage,    text='Config')

        """[Status page]"""
        statusPageTitleLabel = ttk.Label(statusPage, text='Monitoring Status')
        statusPageTitleLabel.pack(pady=1, side=tkinter.TOP)

        LABELWIDTH = 22
        statusColorFrame = ttk.Frame(statusPage)
        self.itemStatusLabel = []
        for i in range(self.NUBER_OF_CHECK_ITEMS):
            self.itemStatusLabel.append(
                tkinter.Label(statusColorFrame,
                              text=self.ItemLabelNames[i],
                              width=LABELWIDTH,
                              bg=COLOR_WHITE))
            self.itemStatusLabel[i].grid(row=i, pady=1)

        statusColorFrame.pack(pady=1)

        legendColorFrame = ttk.Frame(statusPage, relief=tkinter.FLAT)
        legendLabel         = ttk.Label(legendColorFrame, text='Legends:')
        legendOkLabel       = tkinter.Label(legendColorFrame,
                                            text='OK',
                                            bg=COLOR_OK)
        legendBadLabel      = tkinter.Label(legendColorFrame,
                                            text='BAD',
                                            bg=COLOR_BAD)
        legendLowLevelLabel = tkinter.Label(legendColorFrame,
                                            text='Warning',
                                            bg=COLOR_LOWLEVEL)
        legendUpdateLabel   = tkinter.Label(legendColorFrame,
                                            text='Updating',
                                            bg=COLOR_UPDATING)
        legendDisableLabel  = tkinter.Label(legendColorFrame,
                                            text='Disable',
                                            bg=COLOR_DISABLE)
        legendNALabel       = tkinter.Label(legendColorFrame,
                                            text='N/A',
                                            bg=COLOR_WHITE)
        legendLabel        .grid(row=0, column=0, columnspan=1,
                                 padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        legendOkLabel      .grid(row=0, column=1, columnspan=1,
                                 padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        legendBadLabel     .grid(row=0, column=2, columnspan=1,
                                 padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        legendLowLevelLabel.grid(row=0, column=3, columnspan=1,
                                 padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        legendUpdateLabel  .grid(row=1, column=1, columnspan=1,
                                 padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        legendDisableLabel .grid(row=1, column=2, columnspan=1,
                                 padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        legendNALabel      .grid(row=1, column=3, columnspan=1,
                                 padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        legendColorFrame.pack(pady=1)

        """[ShiftInfo page]"""
        shifterFrame = ttk.Frame(shiftinfoPage, relief=tkinter.FLAT)
        shiftPageTitleLabel = ttk.Label(shifterFrame, text='Shifter')
        self.shiftnameEntry  = tkinter.Entry(shifterFrame)
        self.shiftmailEntry  = tkinter.Entry(shifterFrame)
        self.shiftphoneEntry = tkinter.Entry(shifterFrame)
        mailButton = ttk.Button(shifterFrame,
                                text='TestMail',
                                command=self.test_mail)
        callButton = ttk.Button(shifterFrame,
                                text='TestCall',
                                command=self.test_call)
        shiftPageTitleLabel .grid(row=0, column=0, columnspan=2,
                                  padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.shiftnameEntry .grid(row=1, column=0, columnspan=2,
                                  padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.shiftmailEntry .grid(row=2, column=0, columnspan=2,
                                  padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        mailButton          .grid(row=2, column=2,
                                  padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        self.shiftphoneEntry.grid(row=3, column=0, columnspan=2,
                                  padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        callButton          .grid(row=3, column=2,
                                  padx=5, pady=2, sticky=tkinter.W+tkinter.E)
        shifterFrame.pack(pady=1)

        """[Config page]"""
        configFrame = ttk.Frame(configPage, relief=tkinter.FLAT)
        configTitle = ttk.Label(configFrame, text='Uncheck for disable')
        configTitle.pack(pady=1)
        self.is_check_item = [tkinter.BooleanVar()
                              for i in range(self.NUBER_OF_CHECK_ITEMS)]
        # default (un-)check flag is set in self.load_last_config()
        checkButtons = []
        for i in range(self.NUBER_OF_CHECK_ITEMS):
            self.is_check_item[i].set(True)
            checkButtons.append(
                ttk.Checkbutton(configFrame,
                                text=self.ItemLabelNames[i],
                                variable=self.is_check_item[i]))
            checkButtons[i].pack(pady=1, fill=tkinter.BOTH)

        configFrame.pack(pady=1)


        notebook.pack(fill=tkinter.BOTH)


        """-----[ All widgets set place ]-----"""
        timerFrame .pack(pady=1)
        buttonFrame.pack(pady=1)
        noteFrame  .pack(pady=1)
        motherFrame.pack()

        self.running = True  # Running flag
        self.timerCounter = int(self.CHECK_INTERVAL)  # Count-down timer

        self.on_start_up()  # Start
        self.root.mainloop()  # Application drawn

        
    """oooOOO[ Internal Functions ]OOOooo"""
    def system_print(self, print_text):
        date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print('# SYSTEM({0}): {1}'.format(date, print_text))
        return True

    def warning_print(self, print_text):
        date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print('# WARNING:({0}): {1}'.format(date, print_text))
        return True

    def on_start_up(self):
        self.load_last_config()
        self.count_down_every_1sec()  # Start count down loop
        return True

    def on_shut_down(self):
        self.save_last_config()
        self.system_print('shutdown')
        sys.exit()

    def count_down_every_1sec(self):
        if self.running is True:
            """--[ Reflesh window every 1000musec and Count down]--"""
            if self.timerCounter == 0:
                self.counterEcho.set('Update')
            elif self.timerCounter < 0:
                self.counterEcho.set('Update')
                self.update_every_interval()
            else:
                self.counterEcho.set('{0:02d}'.format(self.timerCounter))

            date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.clockEcho.set('{}'.format(date))
            self.timerCounter = self.timerCounter - 1
            self.root.after(1000, self.count_down_every_1sec)
        else:
            """--[ Reflesh window every 1000musec ]--"""
            date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.clockEcho.set('{}'.format(date))
            self.root.after(1000, self.count_down_every_1sec)

        return True

    def update_every_interval(self):
        self.save_last_config()
        
        """
        Here, executes checking-script for each item and obtains each status.
        This sample code uses python scripts as import modules.
        Of cource you can use other script or compiled c++ program
        via calling shell (e.g. subrprocess.call(cmd, shell=True) ).
        Please its return value set as following definition.
        The checking interval can set as self.CHECK_INTERVAL (default 10min).
        """

        """
        status level definition
        0 --> default: updating
        1 --> good
        2 --> bad
        3 --> disable
        4 --> warning
        """

        for i in range(self.NUBER_OF_CHECK_ITEMS):
            status_of_item = 0
            if self.is_check_item[i].get() is True:
                status_of_item = self.ItemScripts[0].get_status()
            else:
                status_of_item = 3
                
            self.itemStatusLabel[i].configure(
                bg=self.colorOfStatus[status_of_item])

            if status_of_item == 0:
                # updating case: 
                pass
            elif status_of_item == 1:
                # good case:
                pass
            elif status_of_item == 2:
                # bad case: send an email and call phone
                self.send_an_email(self.ItemLabelNames[i])
                self.phone_call()  # <-- but not supported yet
            elif status_of_item == 3:
                # disable case:
                pass
            elif status_of_item == 4:
                # low level alarm case: only send an email
                self.send_an_email(self.ItemLabelNames[i])
            else:
                print('# ERROR: unknown status number')
                sys.exit()


        # reset count down timer
        self.timerCounter = int(self.CHECK_INTERVAL)

        return True

    def send_an_email(self, error_item_name):
        to_address   = str(self.shiftmailEntry.get())
        from_address = self.from_address
        subject      = '=== {} ==='.format(error_item_name)
        mail_message = ('Alarm of {} by GeneralAlarmSystem\n'
                        .format(error_item_name))

        if to_address is None or to_address == '\n':
            sys.stderr.write('# ERROR: to address is not set\n')
            return False

        if self.mode == 'debug':
            # Skip mail transportaion in case of debug
            self.system_print(
                'alert to {0} === {1} === w/o mail-transportation (debug-mode)'
                .format(to_address, error_item_name))
        else:
            self.MailApp.send(to_address, from_address, subject, mail_message)
            self.system_print(
                'mail to {0} === {1} ==='
                .format(to_address, error_item_name))
        return True

    def phone_call(self):
        # This program is still not supported
        print('Sorry, call function is out of service')
        
        phone_number_text = str(self.shiftphoneEntry.get()).rstrip()
        phone_number = phone_number_text.replace('-', '')
        print(phone_number)
        self.system_print('call to {}'.format(phone_number_text))
        #cmd = './make_a_call.Linux {}'.format(int(phone_number))
        #prc = subprocess.Popen(cmd, chell=True)
        return True
        
    def save_last_config(self):
        shifter_name  = str(self.shiftnameEntry.get())
        shifter_mail  = str(self.shiftmailEntry.get())
        shifter_phone = str(self.shiftphoneEntry.get())
        if shifter_name is None:
            self.warning_print('empty shifter name')
            shifter_name = 'empty'
        if shifter_mail is None:
            self.warning_print('empty shifter mail address')
            shifter_mail = 'empty'
        if self.check_shifter_mail(shifter_mail) is False:
            self.warning_print('mail address should be wituout space')
        if shifter_phone is None:
            #self.warning_print('empty shifter phone address')
            shifter_phone = 'empty'
            
        fout = open(self.CONFIG_FILENAME, 'w')
        fout.write('{}\n'.format(shifter_name))
        fout.write('{}\n'.format(shifter_mail))
        fout.write('{}\n'.format(shifter_phone))
        for i in range(self.NUBER_OF_CHECK_ITEMS):
            fout.write('{}\n'.format(self.is_check_item[i].get()))
        fout.close()

        return True

    def load_last_config(self):
        if not os.path.isfile(self.CONFIG_FILENAME):
            self.system_print('failed load last config, set default value')
            return False

        fin = open(self.CONFIG_FILENAME, 'r')
        shifter_name  = fin.readline()
        shifter_mail  = fin.readline()
        shifter_phone = fin.readline()
        self.shiftnameEntry .insert(tkinter.END, shifter_name.rstrip())
        self.shiftmailEntry .insert(tkinter.END, shifter_mail.strip())
        self.shiftphoneEntry.insert(tkinter.END, shifter_phone.rstrip())
        for i in range(self.NUBER_OF_CHECK_ITEMS):
            boolean_of_check_item = fin.readline()
            if boolean_of_check_item is None or boolean_of_check_item == '\n':
                print('# ERROR: config file "{}" has wrong format'
                      .format(self.CONFIG_FILENAME))
                boolean_of_check_item = 'False'
            self.is_check_item[i].set(boolean_of_check_item.rstrip())
        fin.close()
        self.system_print('load last config from "{}"'
                          .format(self.CONFIG_FILENAME))

        return True

    def check_shifter_mail(self, shifter_mail):
        index_of_space = shifter_mail.find(' ')
        if index_of_space < 0:
            return True
        else:
            return False

        
    """-----[ Button Functions ]-----"""
    def update_cmd(self):
        self.update_every_interval()
        return True

    def quit_cmd(self):
        self.running = False
        self.on_shut_down()

    def stopstart_cmd(self):
        if self.running is True:
            self.system_print('Stop count down')
            self.running = False
        else:
            self.system_print('Re-start count down')
            self.running = True
        return

    def test_mail(self):
        self.system_print('test_mail')
        self.send_an_email('Test')
        return True

    def test_call(self):
        self.system_print('test_call')
        self.phone_call()
        return True


##################################################################
##################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Here, you can display messeages when Option -h\n')
    parser.add_argument('-d', '--debug',
                        action='store_const',
                        const=True,
                        default=False,
                        help='set debug-mode=True (default: False)')
    parser.add_argument('-c', '--clean',
                        action='store_const',
                        const=True,
                        default=False,
                        help='delete config file data')
    args = parser.parse_args()

    if args.debug:
        root = TGeneralAlarmSystemApplication('debug')
    elif args.clean:
        root = TGeneralAlarmSystemApplication('clean')
    else:
        root = TGeneralAlarmSystemApplication()

    sys.exit()
