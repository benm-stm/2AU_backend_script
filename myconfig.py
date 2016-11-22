# myconfig.py:
#python 2AU.py 'codex 9.0' codex-test.cro.st.com,127.0.0.1 raf.yml,test.yml 8
#Needed modules
#pip install ansible
#pip install paramiko PyYAML Jinja2 httplib2 six (to be verified)

#ansible source http://stackoverflow.com/questions/35368044/how-to-use-ansible-2-0-python-api-to-run-a-playbook

#see https://serversforhackers.com/running-ansible-2-programmatically

#needed steps
# http://docs.ansible.com/ansible/intro_installation.html#running-from-source

app_location = "/root/2AU_python_script"
#sendmail, download packages and create repo before the deadline in days
deadline = 3
opretionLaunchTime = "6:00h"
opretionFinishTime = "7:00h"

#email configuration
send_mail = 1
sender_email_address = "upgradeAutomation@st.com"
recipients_email_address = ["mohamed-rafik.benmansour@st.com"]
smtp_server= "smtpapp1.cro.st.com"

testPlatformLink = "crx19006.cro.st.com:8082"

# The conception of the input is a sum of squares (8 4 2 1) like the access rules in linux (which is 4 2 1)
# If we want to add a new entry in our defined_rules table the next digit will be 16 ...
#  8:"sendmail_to_team",
#  4:"sendmail_to_prodops",
#  2:"sendmail_to_run_tests",
#  1:"run_playbooks"
defined_rules = {
    "8":"sendmail_to_team",
    "4":"sendmail_to_prodops",
    "2":"sendmail_to_run_tests",
    "1":"run_playbooks"
    }

#to run related playbooks
run_playbooks = 1
playbooks_path = "/root/2AU_python_script/playbook/playbooks/"

#logging
log_file = "/root/2AU_python_script/2AU.log"
log_lvl = "logging.DEBUG"
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

#tasks chron
cron_file = "/var/spool/cron/root"
#if you change this var make sure to erase its content first
section_name = "2AU"
#cron behaviour
cron_hour = 9
cron_minute = 0

#DB informations
host="10.157.15.161"
user="2AU"
passwd="password"
db_name="2AU"

#Web server infos
port = "8081"










#draft
instance = "codex-test.draft"
