#!/usr/bin/env python3
# -*-  coding: utf-8 -*-

"""
sig2dot v0.10 (c) E-Post@bmarwell.de, released under the GPL
Download from: -- no URL yet --

    This file is part of sig2dot.

    sig2dot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    sig2dot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with sig2dot.  If not, see <http://www.gnu.org/licenses/>.
"""


class OpenPGPSig(object):
    """
    Contains all relevant information from a signature:
    * ID of the signer, 16 digits
    * Date of signing
    * Expiry of signature, else -1

    Note: The UID from the signer is not needed, since we can identify him
    by his key.
    """

    def __getSigndate(self):

        return self.__signdate

    def __setSigndate(self, date):

        self.__signdate = date

    def __getID(self):

        return self.__id

    def __setID(self, id):

        self.__id = id

    def __getExpirydate(self):

        return self.__expirydate

    def __setExpirydate(self, date):

        self.__expirydate = date

    # ----------------------------------------------------------------------- #
    # Override Built-ins
    # ----------------------------------------------------------------------- #
    def __hash__(self):
        """
        Instances are considered equal if the ID (8 digits) matches.
        This is because UIDs can be added, revoked etc. to/from the public key,
        but the ID remains the same and still belongs to the same owner.
        """

        return int(self.__id, 16)

    def __eq__(self, other):

        if not isinstance(other, OpenPGPSig):
            return False

        if self.__id == other.id:
            return True
        else:
            return False

    def __init__(self):
        '''
        Constructor
        '''
        self.__id = ""  # note: this is the ID of the signer!
        self.__signdate = -1
        self.__expirydate = -1
        self.__signuid = ""

    # ----------------------------------------------------------------------- #
    # Hidden properties
    # ----------------------------------------------------------------------- #
    id = property(__getID, __setID)
    signdate = property(__getSigndate, __setSigndate)
    expirydate = property(__getExpirydate, __setExpirydate)
