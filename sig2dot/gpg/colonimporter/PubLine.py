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

from sig2dot.gpg.colonimporter.ParsedLine import ParsedLine


class PubLine(ParsedLine):
    """ An object for a gpg-listsig-line beginning with pub. """

    def __getID(self):

        return self.__id

    def __setID(self, __id):

        try:
            int(__id, 16)
        except:
            raise ValueError

        self.__id = __id

    def __getCreationdate(self):

        return self.__creationdate

    def __setCreationdate(self, __date):

        try:
            int(__date)
        except:
            raise ValueError

        self.__creationdate = __date

    def __getExpirydate(self):

        return self.__expirydate

    def __setExpirydate(self, __date):

        try:
            int(__date)
        except:
            raise ValueError

        self.__expirydate = __date

    def __eq__(self, other):
        '''

        @param other: any object to compare with
        '''

        if not isinstance(other, PubLine):
            return False
        elif self.id == other.id:
            return True
        else:
            return False

    def __init__(self):
        '''
        Default constructor with no attributes
        '''

        ParsedLine.__init__(self)
        self.__id = ""
        self.__creationdate = 0
        self.__expirydate = 0

    # hidden getters and setters
    id = property(__getID, __setID)
    creationdate = property(__getCreationdate, __setCreationdate)
    expirydate = property(__getExpirydate, __setExpirydate)
