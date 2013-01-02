#!/usr/bin/env python3
# -*-  coding: utf-8 -*-

"""
    sig2dot - parses gpg-signature-output and creates a dot-file for graphviz
    Copyright (C) 2009, Benjamin Marwell

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


#=============================================================================
# Parses output of gpg's signature list into a format
# suitable for rendering into a graph by graphviz 
# (http://www.graphviz.org/) like so:
# 
# $ gpg --no-options --with-colons --fixed-list-mode  --list-sigs    \
#         --no-default-keyring --keyring ./myLUG.gpg |                 \
#          ./sig2dot.py -a -u "[User ID not found]" > myLUG.dot
# $ neato -Tpng myLUG.dot > myLUG.png
#=============================================================================


import sys

from gettext import gettext as _

from gpg import OpenPGPKey, OpenPGPSig
from gpg.colonimporter import PubLine, ParsedLine, LineParser, SigLine, UidLine

import exporter.dot.writer as dot


def main():
    
    opts = getopt()
    
    keylist = {}
    pl = ParsedLine.ParsedLine
    current_key = OpenPGPKey.OpenPGPKey()
     
    # Read line per line and do chomp() aka rstrip()
    for line in sys.stdin.buffer.readlines():

        line = proper_input(line)
        
        pl = LineParser.parse_line(line)
        
        if isinstance(pl, PubLine.PubLine):
            current_key, keylist = process_pubkey(pl, keylist)
        elif isinstance(pl, UidLine.UidLine):
            current_key = process_userid(pl, current_key)
        elif isinstance(pl, SigLine.SigLine):
            if pl.name != opts.user:
                # Add signature to signed key and to signing key
                current_key = process_sig(pl, current_key)
                # Remember who signed whom
                keylist = process_signer(pl.id, current_key, keylist)
        else:
            pass
        
    
    if not opts.allkeys:
        keylist = remove_unsigned(keylist)
    
    # output to dot goes here
    dot.create_dot(keylist, opts.title, opts.blackwhite, opts.renderdate)    
    


def remove_unsigned(keylist):
    
    for id, key in keylist.items():
        if len(key.sigs) == 0:
            keylist.remove(id)
            
    return keylist


def proper_input(line):
    
    for encoding in ("utf8", "latin1", "latin_1", "iso-8859-1", "utf16",
                     "iso-8859-15", "cp1250", "cp1252", "macroman", "ascii"):
        try:
            line = line.decode(encoding, "strict")
            break
        except:
            continue
    
    if isinstance(line, bytes):
        line = str(line)
    
    line = line.rstrip('\n')
        
    return line


def process_pubkey(pl, keylist):
    
    current_key = OpenPGPKey.OpenPGPKey()
    current_key.id = pl.id

    if not pl.id in keylist:
        keylist[pl.id] = current_key
    else:
        current_key = keylist[pl.id]
        
    return current_key, keylist


def process_userid(uidline, key):
    
    if not key.name:
        key.name = uidline.name
        key.email = uidline.email
        key.comment = uidline.comment
        
    return key
    

def process_sig(sigline, key):
    
    sig = OpenPGPSig.OpenPGPSig()
    
    # No selfsigs, please
    if key.id == sigline.id:
        return key
    
    # Also no unknown, please - already sorted out.
    #if sigline.name == "[User ID not found]":
    #    return key
    
    sig.id = sigline.id
    sig.expirydate = sigline.expirydate
    sig.signdate = sigline.signdate
    
    key.addSig(sig)

    return key


def process_signer(signer, signed, keylist):
    
    # signer is an ID, signed a key
    signer_key_dummy = OpenPGPKey.OpenPGPKey()
    signer_key_dummy.id = signer
    
    # fetch existing or add new
    if not signer in keylist:
        keylist[signer] = signer_key_dummy
    else:
        signer_key_dummy = keylist[signer]
        

    signer_key_dummy.addSigned(signed.id)
        
    keylist[signer_key_dummy.id] = signer_key_dummy
    
    return keylist


def getopt():
    """
    Parses command line parameters for known arguments and options.
    """

    from optparse import OptionParser

    usage="""
LANG=C gpg --no-options --with-colons --fixed-list-mode  --list-sigs    
    --no-default-keyring --keyring ./myLUG.gpg |                 
    ./sig2dot.py > myLUG.dot"""

    parser = OptionParser(usage=usage)

    parser.add_option(  "-a", "--all-keys",
                        dest="allkeys",
                        action="store_true",
                        default="False",
                        help=_("Render all keys, even if they're not signed "
                        "by any other key.  ") )

    parser.add_option(  "-b", "--black-white",
                        dest="blackwhite",
                        action="store_true",
                        default="False",
                        help="""Black and white / do not colourize. In fact,
                        it will be transparent. If you use this,
                        be sure not to use jpeg or other formats for graphing,
                        which do not support transparency.""")

    parser.add_option(  "-d", "--date",
                        dest="renderdate",
                        action="store",
                        help="""Render graph as it appeared on <date> 
                        (ignores more recent signatures).  
                        Date must be in the format "YYYY-MM-DD".  
                        Will also ignore keys that have since been revoked.""" )

    parser.add_option(  "-q", "--quiet",
                        dest="verbose",
                        action="store_false",
                        default="True",
                        help="Be quiet" )
    
    parser.add_option(  "-t", "--title",
                        dest="title",
                        action="store",
                        default="unnamed",
                        help="Set title for graph. Default: unnamed." )
    
    parser.add_option(  "-u", "--user-not-found-string",
                        dest="user",
                        action="store",
                        default="[User ID not found]",
                        help="Set the [User ID not found]-String. See manpage"
                        " for Details." )    

    (options, args) = parser.parse_args()
    
    check_opts(options)

    return options


def check_opts(opts):
    
    split_date = opts.renderdate.split("-")
    if len(split_date) != 3:
        print("Please specify date in this format: \"YYYY-MM-DD\"", 
              file=sys.stderr)
        sys.exit(1)
        
    try:
        str(opts.user)
    except:
        print("Please specify a user-id-_STRING_.", file=sys.stderr)
        sys.exit(1)



if __name__ == '__main__':
    main()
    sys.exit(0)
