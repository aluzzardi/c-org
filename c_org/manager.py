#!/usr/bin/python3
#
# Copyright (C) 2018 Continuous Organisation.
# Author: Pierre-Louis Guhur <pierre-louis.guhur@laposte.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''c_org configuration manager'''

import logging
import os
import yaml
try:
    import cPickle as pickle
except:
    import pickle
import solc
from web3 import Web3
from web3.auto import w3
import c_org.utils as utils


class ContractManager(object):

    def __init__(self):
        self._config = None
        self._name = ""
        self.parse()
        self.clean_name = utils.clean_name(self.name)
        self.check_files()

    @property
    def config(self):
        if not self._config:
            self.parse()
        return self._config.get('c-org')

    @property
    def name(self):
        if self._name:
            return self._name
        return self.config.get('name')

    def load(self):
        """ Read continuous organisation build file """
        filename = utils.get_build_file(self.name)
        logging.debug("Unpickling build file {}".format(filename))
        c = utils.restricted_unpickle(filename)
        self.contract = w3.eth.contract(abi=c['abi'],
                                        address=c['address'])
        return self.contract

    def check_files(self):
        """ Check the existence of folders and create necessary ones """
        # check existence
        source = utils.get_source_path()
        if not os.path.isdir(source):
            raise IOError("The continuous organisation's contract's folder does not exist: {} ".format(source))
        config = utils.get_config_file()
        if not os.path.isfile(config):
            raise IOError("The continuous organisation's config file does not exist: {} ".format(config))
        # create folder
        build = os.path.join(utils.get_build_path(), self.clean_name)
        if not os.path.isdir(build):
            os.makedirs(build)

    def parse(self):
        filename = utils.get_config_file()
        logging.debug("Parsing configuration filename {}".format(filename))
        with open(filename, 'r') as f:
            self._config = yaml.load(f)
        return self.config

    def build(self):
        # save build file
        store = {'abi': self.interface['abi'], 'address': self.address}
        filename = utils.get_build_file(self.name)
        with open(filename, 'wb+') as f:
            pickle.dump(store, f)

    def compile(self):
        filename = utils.get_source_file(self.config.get('version'))
        with open(filename, 'r') as f:
            source_code = f.read()
        compiled_sol = solc.compile_source(source_code)
        self.id, self.interface = compiled_sol.popitem()

    def param_constructor(self):
        return []

    def deploy(self):
        w3.eth.defaultAccount = w3.eth.accounts[0]#self.config.get('wallet')
        self.contract = w3.eth.contract(abi=self.interface['abi'],
                                        bytecode=self.interface['bin'])
        tx_hash =  self.contract.constructor(*self.param_constructor()).transact()
        self.address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return self.address
