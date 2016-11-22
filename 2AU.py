#!/usr/bin/python

#import params from myconfig.py file
from myconfig import *

#import customized modules
import playbook
import sendMail
import logger
import dao
import croner
import webservices

# used to import modules
import os
import sys , getopt#used also to get params for the python script

class upgradeAutomation:

    # params : release       : String
    #          instances      : String
    #          rule          : Int
    def __init__(self, release, instances, rule, defined_rules, logger):
        self.release=release
        self.instances=instances
        self.rule=rule
        self.defined_rules=defined_rules
        self.logger = logger

    #used to extract rules
    def getRules(self):
        length         = len(self.defined_rules) 
        tmp            = int(self.rule)
        selected_rules = []
        if self.is_valideRule():
            while tmp > 0:
                square = 2**length
                if tmp >= square:
                    selected_rules.append(square)
                    tmp -= square
                length -= 1
            self.logger.info('selected rules : %s' %(selected_rules))
        else:
            self.logger.error('invalid rule format please verify your inputs')
        return selected_rules

    #used to validate the rule given as param
    def is_valideRule(self):
        rule = 0
        length = len(self.defined_rules) 
        for i in range(0,length):
            rule += 2**i
        if (int(self.rule) <= rule):
            return True
        else:
            return False

    def run_croner(self, release, instance, logger, cron_file, section_name, cron_hour, cron_minute, deadline, app_location, db):
        #if the param passed is to store crons
        cron = croner.croner(release, instance, logger, cron_file, section_name, cron_hour, cron_minute, deadline, app_location)
        #remove the created section to clean the cron file
        cron.refreshCrontab()
        #fill a new section in the cron file
        cron.fillJobs(cron.getJobs(db.getDao()))

#************************************main****************************************
#instanciate vars
instances = None
release = None
playbooks = None
is_croner = None
rule = None
is_croner = False
run_webserver = False

#instanciate Logger
log = logger.logger(log_file, log_lvl, log_format)
logger = log.create_logger()
logger.info('---- logger init ----')

# get input for the py script
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hcsi:r:p:u:",["instances=","release=","playbooks=","rule="])
except getopt.GetoptError:
    print '%s -i <instances array> -r <release> -p <playbooks array> -u <rule> -s -c \n -c : launch croning process who\'ll read from db and insert entries into crontab\n -s : run webserver to serve restful calls' % __file__

for opt, arg in opts:
    if opt == "-h":
        print '%s -i <instances array> -r <release> -p <playbooks array> -u <rule> -s -c \n -c : launch croning process who\'ll read from db and insert entries into crontab\n -s : run webserver to serve restful calls' % __file__
        sys.exit()
    elif opt =="-c":
        is_croner = True
    elif opt == "-s":
        run_webserver = True
    elif opt in ("-i", "--instances"):
        instances = arg.split(",")
    elif opt in ("-r", "--release"):
        release = arg
    elif opt in ("-p", "--playbooks"):
        playbooks = arg.split(",")
    elif opt in ("-u", "--rule"):
        rule = arg

#Verify if the conf params are at least valide
if not os.path.exists(playbooks_path):
    logger.error("%s does not exist" %playbooks_path)
    sys.exit()
#Concatenate playbooks with path
if playbooks:
    for i in range(len(playbooks)):
        playbooks[i] = playbooks_path + playbooks[i]

#check weather the croner call was well issued
if is_croner and instances and release:
    #the croner part needs access to the DB
    db = dao.dao(host, user, passwd, db_name)
    AU = upgradeAutomation(release, instances, rule, defined_rules, logger)
    AU.run_croner(release, instance, logger, cron_file, section_name, cron_hour, cron_minute, deadline, app_location, db)
#check weather the launcher call was well issued
elif instances and release:
    #Instanciate needed classes (or lets say tools)
    AU = upgradeAutomation(release, instances, rule, defined_rules, logger)
    sm = sendMail.sendMail(instances, release, logger, deadline, opretionLaunchTime, opretionFinishTime, testPlatformLink)
    pb = playbook.playbook(instances, playbooks, logger)

    #extract given rules into an array of rules
    rules = AU.getRules()
    #Call methodes based on the given rules
    for i in range(0,len(rules)):
        if defined_rules[str(rules[i])] == "run_playbooks":
            if playbooks:
                pb.run()
            else:
                logger.error("you have specified a playbook launch in the rules but you didn't present any playbook in params")
                print "ERROR : you have specified a playbook launch in the rules but you didn't present any playbook in params"
        else:
            sm.send(sender_email_address, recipients_email_address, smtp_server, defined_rules[str(rules[i])]) 
elif run_webserver:
    server = webservices.webservices()
    server.run(port)
else:
    print '%s -i <instances array> -r <release> -p <playbooks array> -u <rule> -s -c \n -c : launch croning process who\'ll read from db and insert entries into crontab\n -s : run webserver to serve restful calls' % __file__
