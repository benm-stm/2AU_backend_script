#!/usr/bin/python

import MySQLdb
import datetime
import re

class croner:

    # params : release       : String
    #          instances      : String
    #          role          : Int
    def __init__(self, release, instance, logger, cron_file, section_name, cron_hour, cron_minute, deadline, app_location):
        self.release=release
        self.instance=instance
        self.logger = logger
        self.cron_file = cron_file
        self.section_begin = "#"+section_name+"-begin\n"
        self.section_end = "#"+section_name+"-end"
        self.cron_hour=cron_hour
        self.cron_minute=cron_minute
        self.cron_file = cron_file
        self.deadline = deadline
        self.app_location = app_location

    def refreshCrontab(self):
        # create regular expression pattern
        chop = re.compile(self.section_begin+'.*?'+self.section_end, re.DOTALL)
        # open file
        f = open(self.cron_file, 'r')
        data = f.read()
        f.close()
        # chop text between #chop-begin and #chop-end
        data_chopped = chop.sub('', data)
        # save result
        f = open(self.cron_file, 'w')
        f.write(data_chopped)
        f.close()

    def fillJobs(self, jobs):
        # save result (append to file)
        f = open(self.cron_file, 'a')
        f.write(self.section_begin)
        for i in range(0,len(jobs)):
            #every event will have 2 entries or jobs one with the role 5 and the other with the role 10
            f.write(jobs[i]+"\n")
        f.write(self.section_end)
        f.close()

    def getJobs(self, cur):
        now = datetime.datetime.now()
        jobs_array = []
        cur.execute("SELECT * FROM evenement")
        # print all the first cell of all the rows
        for row in cur.fetchall():
            if now <= row[2]:
                cron_date_d = str(self.cron_hour)+" "+str(self.cron_minute)+" "+str(row[2].day - self.deadline)+" "+str(row[2].month)
                #this section must be taken from the DB
                params_d = " -r "+str(self.release)+" "+str(row[4])+" "+"raf.yml"+" 5"
                cron_date = str(self.cron_hour)+" "+str(self.cron_minute)+" "+str(row[2].day)+" "+str(row[2].month)
                params = " -r "+str(self.release)+" "+str(row[4])+" 10"
                script= self.app_location+" & ./"+__file__

                jobs_array.append(cron_date_d+" * cd "+script+" "+params_d)
                jobs_array.append(cron_date_d+" * cd "+script+" "+params_d)
        return jobs_array
