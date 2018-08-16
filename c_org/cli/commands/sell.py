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

'''c_org sell command line'''

import logging
from web3.auto import w3
from web3 import Web3

from c_org.cli.command import COrgCommand
from c_org.manager import ContinuousOrganisationManager


class COrgSell(COrgCommand):

    def __init__(self):
        super().__init__(command_id='sell',
                         description='Sell tokens')


    def run(self):
        self.parser.add_argument('--account',
                                 help='Address of the sender',
                                 type=float)
        self.parser.add_argument('--amount',
                                 help='Amount to send',
                                 type=float)
        self.parser.add_argument('--c-org',
                                 help='Continuous Organisation\'s name',
                                 type=str)

        self.parse_args()
        self.run_command()


    def run_command(self):
        c_org_manager = ContinuousOrganisationManager(name)
        self.contract = c_org_manager.load()

        logging.debug('Sending an amount of {:d} to {}'.
                       format(self.amount, self.c_org))
        tx_hash = self.contract.functions.burning(self.amount) \
                                         .transact({'from': self.account})
        w3.eth.waitForTransactionReceipt(tx_hash)