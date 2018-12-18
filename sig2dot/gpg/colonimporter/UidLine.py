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

from .ParsedLine import ParsedLine


class UidLine(ParsedLine):
    """ An object for a gpg-sig-line beginning with uid. """

    def __getName(self):

        return self.__name

    def __setName(self, name):

        if not isinstance(name, str):
            raise TypeError

        self.__name = name

    def __getComment(self):

        return self.__comment

    def __setComment(self, comment):

        if not isinstance(comment, str):
            raise TypeError

        self.__comment = comment

    def __getEmail(self):

        return self.__email

    def __setEmail(self, email):

        if not isinstance(email, str):
            raise TypeError

        self.__email = email

    def __init__(self):
        '''
        Constructor
        '''

        ParsedLine.__init__(self)
        self.__name = ""
        self.__comment = ""
        self.__email = ""

    # hidden getters and setters
    name = property(__getName, __setName)
    comment = property(__getComment, __setComment)
    email = property(__getEmail, __setEmail)
