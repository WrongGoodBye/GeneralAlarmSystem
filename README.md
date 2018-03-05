# GeneralAlarmSystem

## Description

This provides just sample codes of GUI application for monitoring some logger files.
Checking scripts of logger files should be written by users for each purpose.

## Features

- Easy check status on GUI
- Update status every 1min (usr can set)
- Sending an email to shifter in case of that bad status find


## Requirement

- python3, tkinter module, datetime module, subprocess module, and argparse module.
  - you can install aboves via anaconda (https://www.anaconda.com/download/) 
- `sendmail` command (install to `/usr/sbin/sendmail`)
- logger analysis scripts written by users for each purpose
  
## Usage

- Firstly, you should edit `./main.py` and set parameters
  - `self.CHECK_INTERVAL`: a check interval for analysis logger files (default 1min)
  - `self.NUBER_OF_CHECK_ITEMS`: the number of monitoring targets (default 5 items)
  - `self.ItemLabelNames`: display labels of monitorings
  - `self.ItemScripts`: analysis scripts of monitoring logger files, their scripts should be imported such as line 22-27 <code python>import CheckingScripts.CheckItem02</code>
  - `self.from_address`: mail sender address, for instance, an email of an account of this general alarm system
- Secondary, you should write analysis scripts
  - A realistic example is provided as `./CheckingScripts/CheckSample001.py`
  - Get logger file from a remote-PC via ssh-rsa-key (of course, you should create non-pass-phrase key and share local and remote machine), read the logger file, return status value
  - Returned value should be set as 
    - 0: updating (default)
    - 1: good status
    - 2: bad
    - 3: disabled, select on app GUI by shifter
    - 4: low-level, in unusual case but not so sufficient
1. `$ python main.py [-d: debug-mode] [-c: clean]`
   - usually, no options are needed
   - debug-mode: runs without a mail-transportation for debug
   - clean: delete files
2. Fill the shifter name, shifter mail, and shifter phone in `ShiftInfo` page
3. Confirm mail address by TestMail button


## Installation

    $ git clone https://github.com/WrongGoodBye/GeneralAlarmSystem

## Anything Else

AnythingAnythingAnything
AnythingAnythingAnything
AnythingAnythingAnything

## Author

OBARA, shuhei
(for [KamLAND experiment](http://www.awa.tohoku.ac.jp/kamland) )

## License

[MIT](https://github.com/WrongGoodBye/GeneralAlarmSystem/LICENSE.txt)
