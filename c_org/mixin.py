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

''' Mixins for Continuous Organisation '''

import os
import yaml
from c_org.utils import Wallet, get_corg_file


class KeysMixin(object):
    ''' Manage the YAML file .c-org/keys.yaml containing informations on the wallets and other securities keys '''


    @property
    def keys(self):
        if not hasattr(self, '_keys'):
            filename = get_corg_file()
            with open(filename, 'r') as f:
                self._keys = yaml.load(f)
        return self._keys

    @property
    def wallets(self):
        return self.keys.get('wallets', [])

    def wallet_exists(self, name):
        names = [w.get('name') for w in self.wallets]
        return name in names

    def add_wallet(self, wallet):
        if isinstance(wallet, dict):
            wallet = Wallet.from_dict(wallet)
        self.wallets.append(vars(wallet))
        self.save()

    def remove_wallet(self, name):
        for wallet in self.wallets:
            if wallet.get('name') == name:
                self.wallets.remove(wallet)
        self.save()
        return

    def save(self):
        filename = get_corg_file()
        with open(filename, 'w+') as f:
            yaml.dump(self.keys, f)
