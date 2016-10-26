#!/usr/bin/env python

import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

class playbook:

    def __init__(self, instance, playbooks_dir):
        self.instance=instance
        self.playbooks_dir=playbooks_dir
        self.variable_manager = VariableManager()
        self.loader = DataLoader()

    #returns the playbooks in a specified path
    def playbooks_list(self):
        files = []
        #folders = []
        for (path, dirnames, filenames) in os.walk(self.playbooks_dir):
            #folders.extend(os.path.join(path, name) for name in dirnames)
            files.extend(os.path.join(path, name) for name in filenames)
        return files

    def run(self, playbook_path):
        inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,  host_list='/etc/ansible/hosts')

        if not os.path.exists(playbook_path):
            print '[INFO] The playbook does not exist'
            sys.exit()

        Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user='slotlocker', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)

        self.variable_manager.extra_vars = {'hosts': 'mywebserver'} # This can accomodate various other command line arguments.`

        passwords = {}

        pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=self.variable_manager, loader=self.loader, options=options, passwords=passwords)

        results = pbex.run()


pb=playbook('codex-test.cro.st.com', '/root/2AU_python_script/playbook/playbooks');
files=pb.playbooks_list()

for x in files:
    pb.run(x)
