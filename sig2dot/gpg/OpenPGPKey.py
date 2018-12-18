#!/usr/bin/env python3
# -*-  coding: utf-8 -*-

"""
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

from . import OpenPGPSig


class OpenPGPKey(object):
    """
    Note to this class: Only the very first UID is being saved.
    """

    # ----------------------------------------------------------------------- #
    # Getters and setters
    # ----------------------------------------------------------------------- #
    def __getID(self):

        return self.__id

    def __setID(self, __id):

        self.__id = __id

    def __getCreationdate(self):

        return self.__creationdate

    def __setCreationdate(self, __date):

        self.__creationdate = __date

    def __getExpireydate(self):

        return self.__expireydate

    def __setExpireydate(self, __date):

        self.__expireydate = __date

    def __getName(self):

        return self.__name

    def __setName(self, __name):

        self.__name = __name
        del __name

    def __getComment(self):

        return self.__comment

    def __setComment(self, __comment):

        self.__comment = __comment
        del __comment

    def __getEmail(self):

        return self.__email

    def __setEmail(self, __email):

        self.__email = __email
        del __email

    def __getSigs(self):

        return self.__sigs

    def __getSigned(self):

        return self.__signed

    # ----------------------------------------------------------------------- #
    # define own methods
    # ----------------------------------------------------------------------- #
    def addSig(self, __sig):

        if not isinstance(__sig, OpenPGPSig.OpenPGPSig):
            raise TypeError("Given object was not OpenPGPSig")

        if __sig not in self.__sigs:
            self.__sigs.add(__sig)

        del __sig

    def addSigned(self, __id):

        self.__signed.add(__id)

        del __id

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

        if not isinstance(other, OpenPGPKey):
            return False

        if self.__id == other.id:
            return True
        else:
            return False

    def __init__(self):
        '''
        Constructor
        '''
        self.__id = ""
        self.__creationdate = 0     # unixtime
        self.__expireydate = 0      # unixtime
        self.__name = ""
        self.__comment = ""
        self.__email = ""
        # Complete List of signatures (type OpenPGPSig
        self.__sigs = set()
        # Here it's enough to store IDs
        self.__signed = set()

    # ----------------------------------------------------------------------- #
    # Hidden properties
    # ----------------------------------------------------------------------- #
    id = property(__getID, __setID)
    creationdate = property(__getCreationdate, __setCreationdate)
    expireydate = property(__getExpireydate, __setExpireydate)
    name = property(__getName, __setName)
    comment = property(__getComment, __setComment)
    email = property(__getEmail, __setEmail)
    sigs = property(__getSigs)
    signed = property(__getSigned)
