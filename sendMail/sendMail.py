import smtplib
from email.MIMEText import MIMEText
import re
import os
import datetime


class sendMail:

    def __init__(self, instances, release, logger, deadline, opretionLaunchTime, opretionFinishTime, testPlatformLink):
        self.release=release
        self.instances=instances
        self.logger= logger
        self.deadline = deadline
        self.opretionLaunchTime = opretionLaunchTime
        self.opretionFinishTime = opretionFinishTime
        self.testPlatformLink = testPlatformLink
    
    def getSection( self, data, section_name):
        try:
            first = '==='+section_name
            last = section_name+'==='
            start = data.rindex( first ) + len( first )
            end = data.rindex( last, start )
            return data[start:end]
        except ValueError:
            self.logger.error("section name "+section_name+" does not exist")
            return ""

    def send(self, fromaddr,toaddr,server, content):
        now = datetime.datetime.now()
        end_date_raw = now + datetime.timedelta(days=self.deadline)
        
        end_date = end_date_raw.strftime("%A %d %B %Y")
        short_current_date = end_date_raw.strftime("%d-%m-%Y")

        server = smtplib.SMTP(server)
        for i in range(0,len(self.instances)):
            fp = open(os.path.dirname(os.path.abspath(__file__))+'/mailContent/'+content, 'rb')
            #remove line breaks
            data=fp.read().replace("\n", "")
            fp.close()
            #replacing values withdynamic ones
            data = data.replace("=upgradeDate=", end_date)
            data = data.replace("=upgradeInstance=", self.instances[i])
            data = data.replace("=shortUpgradeDate=", short_current_date)
            data = data.replace("=opretionLaunchTime=", self.opretionLaunchTime)
            data = data.replace("=opretionFinishTime=", self.opretionFinishTime)
            data = data.replace("=release=", self.release)
            data = data.replace("=testPlatformLink=", self.testPlatformLink)

            #construct mail
            msg = MIMEText(self.getSection(data, "BODY"))
            msg['From'] = fromaddr
            #Insert dynamic mail in case we want to change recipient
            if self.getSection(data, "TO") == "default":
                msg['To'] = ", ".join(toaddr)
            else:
                msg['To'] = self.getSection(data, "TO")
                toaddr = [self.getSection(data, "TO")]
                self.logger.info("recipients are specified in the template : "+str(toaddr))
            msg['Subject'] = self.getSection(data, "SUBJECT")
            msg['Content-Type'] = "text/html; charset=utf-8"

            #server.starttls()
            #server.login(fromaddr, "YOUR PASSWORD")
            server.sendmail(fromaddr, toaddr, msg.as_string())
            self.logger.info("mail sent from %s to %s" %(fromaddr, toaddr));
        server.quit()

