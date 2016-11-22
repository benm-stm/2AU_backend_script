import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

class playbook:

    def __init__(self, hosts, playbooks, logger):
        self.hosts=hosts
        self.playbooks=playbooks
        self.logger= logger
        self.variable_manager = VariableManager()
        self.loader = DataLoader()


    #returns the playbooks in a specified path
    #def playbooks_list(self):
    #    files = []
        #folders = []
    #    for (path, dirnames, filenames) in os.walk(self.playbooks_dir):
            #folders.extend(os.path.join(path, name) for name in dirnames)
    #        files.extend(os.path.join(path, name) for name in filenames)
    #    return files

    def run(self):
        #if we want to read directly from ansible hosts
        #inventory = Inventory(loader=self.loader,
        #                      variable_manager=self.variable_manager,
        #                      host_list='/etc/ansible/hosts')

        inventory = Inventory(loader=self.loader,
                              variable_manager=self.variable_manager,
                              host_list=self.hosts)

        

        Options = namedtuple('Options',
                                        ['listtags',
                                         'listtasks',
                                         'listhosts', 
                                         'syntax', 
                                         'connection',
                                         'module_path',
                                         'forks',
                                         'remote_user',
                                         'private_key_file',
                                         'ssh_common_args',
                                         'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args',
                                         'become',
                                         'become_method',
                                         'become_user',
                                         'verbosity',
                                         'check']
                            )
        options = Options(listtags=False,
                          listtasks=False,
                          listhosts=False,
                          syntax=False,
                          connection='ssh',
                          module_path=None,
                          forks=100,
                          remote_user='slotlocker',
                          private_key_file=None,
                          ssh_common_args=None,
                          ssh_extra_args=None,
                          sftp_extra_args=None,
                          scp_extra_args=None,
                          become=True,
                          become_method=None,
                          become_user='root',
                          verbosity=None,
                          check=False)

        passwords = {}
        pbex = PlaybookExecutor(playbooks=self.playbooks,
                                inventory=inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=options,
                                passwords=passwords)
        results = pbex.run()
        logger.info(results)
