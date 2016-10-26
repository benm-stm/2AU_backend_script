#!/usr/bin/python

#import params from myconfig.py file
from myconfig import *

# used to import modules
import os
import sys #used also to get params for the python script


class upgradeAutomation:
    def __init__(self, release, instance, year, month, day, hour, minute, playbooks_dir):
        self.year=year
        self.month=month
        self.day=day
        self.hour=hour
        self.minute=minute
        self.release=release
        self.instance=instance
        self.playbooks_dir=playbooks_dir

        #needed imports depends on the myconfig.py content
        if send_mail: self.importAllModules('sendMail')
        if run_playbooks: self.importAllModules('playbook') 

    def importAllModules(self, module_name):
        dir_of_interest = module_name
        modules = {}

        sys.path.append(dir_of_interest)
        for module in os.listdir(dir_of_interest):
            if '.py' in module and '.pyc' not in module:
                current = module.replace('.py', '')
                modules[current] = __import__(current)

    
#************************************main****************************************
# get input for the py script
release = sys.argv[1]
instance = sys.argv[2]
year = sys.argv[3]
month = sys.argv[4]
day = sys.argv[5]
hour = sys.argv[6]
minute = sys.argv[7]
playbooks_dir = sys.argv[8]

UA = upgradeAutomation(release, instance, year, month, day, hour, minute, playbooks_dir)

