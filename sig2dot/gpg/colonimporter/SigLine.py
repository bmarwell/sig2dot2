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

class SigLine(ParsedLine):
    """ An object for a gpg-sig-line beginning with pub. """

    def __getID(self):
        
        return self.__id
    
    def __setID(self, id):
        
        try:
            int(id, 16)
        except:
            raise ValueError
        
        self.__id = id
        
        
    def __getSigndate(self):
        
        return self.__signdate
    
    def __setSigndate(self, date):
        
        try:
            int(date)
        except:
            raise TypeError
        
        self.__signdate = date

    
    def __getExpirydate(self):
        
        return self.__expirydate

    def __setExpirydate(self, date):
        
        try:
            int(date)
        except:
            raise TypeError
        
        self.__expirydate = date
        
    
    def __getName(self):
        
        return self.__name
    
    def __setName(self, name):
        
        if not isinstance(name, str):
            raise TypeError
        
        self.__name = name


    def __init__(self):
        '''
        Constructor
        '''
        self.__signdate = 0
        self.__id = ""
        self.__expirydate = -1
        self.__name = ""
    
    # hidden getters and setters 
    id = property(__getID, __setID)
    signdate = property(__getSigndate, __setSigndate)
    expirydate = property(__getExpirydate, __setExpirydate)
    name = property(__getName, __setName)
        