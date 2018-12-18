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

import sys

from . import PubLine, SigLine, UidLine


# =============================================================================
# Main function
# =============================================================================
def parse_line(line):

    splits = line.split(":")

    if splits[0] == "pub":
        myPubLine = create_publine(splits)
        return myPubLine

    elif splits[0] == "uid":
        myUidLine = create_uidline(splits)
        return myUidLine

    elif splits[0] == "sig":
        mySigLine = create_sigline(splits)
        return mySigLine

    else:
        pass


# ==============================================================================
# Return helper functions
# ==============================================================================

def create_publine(splits):
    """
    Creates a publine-class when given a list which has been created by
    splitting a gpg-output-line with seperator ":".
    @param splits:   split up input list
    @type splits:    list of strings, integers
    """

    myPubLine = PubLine.PubLine()
    myPubLine.id = splits[4]
    myPubLine.creationdate = splits[5]

    if splits[6] != "":
        myPubLine.expireydate = splits[6]
    else:
        myPubLine.expireydate = -1

    return myPubLine


def create_uidline(splits):
    """
    Creates a uidline-class from input line
    @param splits:   split up input line
    @type splits:    list of strings, integers
    """

    myUidLine = UidLine.UidLine()
    myUidLine.name = splits[9].split(" (")[0].split(" <")[0]

    try:
        myUidLine.email = splits[9].split(" <")[1][:-1]
    except:
        myUidLine.email = ""

    try:
        myUidLine.comment = splits[9].split(" (")[1].split(") ")[0]
    except:
        myUidLine.comment = ""

    return myUidLine


def create_sigline(splits):
    """

    @param splits:   split up input line
    @type splits:    list of strings, integers
    """
    mySigLine = SigLine.SigLine()
    mySigLine.id = splits[4]
    mySigLine.signdate = splits[5]
    mySigLine.name = splits[9]

    if splits[6] != "":
        mySigLine.expirydate = splits[6]
    else:
        mySigLine.expirydate = -1

    return mySigLine
