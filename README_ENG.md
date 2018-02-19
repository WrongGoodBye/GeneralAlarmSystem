# READNE

## ABSTRACT 
* This application is transcribed with python3 and tkinter from the AutoAlarmSystem which works at a large liquid-scintillator experiment KamLAND.
  * Original AutoAlarmSystem at [KamLAND](http://www.awa.tohoku.ac.jp/kamland/) is written with an unique language of [KiNOKO](http://www.awa.tohoku.ac.jp/~sanshiro/kinoko/)
* AutoAlarmSystem monitors the conditions of experiments for 24-hr and allows to ease the shifter's duty
* Most of all is same as original, but some are changed for the porpuse for general experiment
* Therefore, these provides just sampe code


## Provides
* Sample GUI codes with python and kinter

## Not provided
* Phone-Calling function
  * This source code is complicated and USB-modem is needed
  * If you are interested in, please search with "CTI  phone"


## User preparation 
* PC
  * These souce codes are developed on macOS(10.13.3)
  * If you find lacking of library, please install it
* python3 and tkinter
  * [anaconda3](https://www.anaconda.com) installation provides all of needs
  * Development environment; python3.6.3, tkinter8.6, and anaconda1.6.5
* sendmail command
* analysis scripts
  * sample codes are provided under `./CheckingScript/` but **analysis scripts should be written by users for each purpose**
    * Its return value should be set as; (0: upgrating, 1:good, 2:bad, 3:disable, 4:low-level alarm)
  * In case of a file-transportaion from a remote PC, you can set RSA-key



## How To Use
`$ python ./main.py`

* After launched, Fill the shifter name and the shifter mail-address in each entry on ShiftInfo tab.
* TestMail button send a test mail
* In case of that the targe item is expired temporary, please check-out in Config tab
* Update button runs user's script and checks.
  * When 0 value is found in count-down, this update process automatically starts
* Stop/Start button stops/starts count-down
* Quit button terminates this application


`$ python ./main.py --help`

* Preview help
* You can control arguments via argparse module. Of cource, you can use sys.argv

`$ python ./main.py --debug`

* Run with debug-mode
* Skip the mail-transportaion in this case


## Coding
**Rule**

  * Naming rules are snake-case for variables and functions. 
  * Declearaion of object in tkinter class, such as Button and Frame, camel-case is used
  * TAB is four-spaces
  * Actually, I wanted to comply with pep8 rules, but the name of tkinter objects are too long for obvious layered system.


**./main.py**

  * Mail body of GUI
  * Place the frames, the labels, the entry boxes, the buttons, and the check-buttons via tkinter module
  * Count down. Its timer is saved in the internal variable of `self.timerCounter`, and the checking interval (default=60sec) can be set as `checkingInterval`
  * In every intervals, user scripts under the CheckingScipt dir run and the application displays theirs results with various colors
	   * Return value should be set as (0=updating, 1=good, 2=bad, 3=disable, 4=lowlevel)
      * Default status value sets to be 0
  * In case of that bad-status is found, send an alert email
    * Messages are able to be changed with a variable of `mail_message`
    * ToAddress is obtained from ''Entry'' in ShiftInfo-tab with a default value of `DEFAULT_MAIL`    
    * For the safety operataion, `DEFAULT_USR` and `DEFAULT_MAIL` should be set as anyone('s) who is an expert 
  * Object names (ChekingTarget01~06) are directly labeled but they should be renamed as each target (DAQ, HV, and others)
  * Checking target needs to be hard-coded, but in a temporary case of un-checked:
    * Checke out in Config-tab
    * Then, its label color will be changed gray (disable)
  * Information of Config-tab and ShiftInfo-tab are storaged in a file of `./config.txt` (`self.save_last_config()`), and it will be automatically loaded at the next time of application running(`self.load_last_config()`)

**./main_tiny.py**

  * Basically same as `main.py` but some functions  are only supported
  

**./AlertScript/Mail.py**

  * A wrapper of `/usr/sbin/sendmail`
  * If you are interested, it can be added BCC/CC functions

**./CheckingScript/CheckItemXX.py**

  * A script for checking each target after every interval
  * This should be prepared by users 
  * For example in KamLAND, the procedures are as follows
    * scp from remotePC 
    * next, analysis its log-file and output to local-file
    * after that, check for the latest 10min results and return good/bad
 
**./CheckingScript/Sample001.py**

  * A example of checking script, which obtains log-file from a remotePC with scp connection via ssh-rsa key
  * For a preparation, ssh-rsa key is generated and set in each PC (remotePC and this PC), and log-file format needs to be `[unixtime] [data]\n`

## Tasks ##
* Calling program via USB-modem
  * Because I do not have USB-modem here, I could not test
* Beautiful GUI
  * ''tkinter'' is not so beautiful in Linux
  * For a cross-platform GUI application, there are ''wxPython'', ''kivy'', and others. However, they require additional installations other than anaconda-package.


## Copyright##
  * OBARA shuhei (<obara.syuhei.asrtoparticle@gmail.com>)
  * First update on February 19th, 2018.
 