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


# =============================================================================
# Parses output of gpg's signature list into a format
# suitable for rendering into a graph by graphviz
# (http://www.graphviz.org/) like so:
#
# $ gpg --no-options --with-colons --fixed-list-mode  --list-sigs    \
#         --no-default-keyring --keyring ./myLUG.gpg |                 \
#          ./sig2dot.py -a -u "[User ID not found]" > myLUG.dot
# $ neato -Tpng myLUG.dot > myLUG.png
# =============================================================================

import argparse
import logging
import sys
from datetime import datetime
from gettext import gettext as _

import iso8601

import sig2dot.exporter.dot.writer as dot
from sig2dot.gpg import OpenPGPKey, OpenPGPSig
from sig2dot.gpg.colonimporter import PubLine, ParsedLine, LineParser, SigLine, UidLine

logger = logging.getLogger(__name__)


def main():

    args = getarg()

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
            if pl.name != args.user:
                # Add signature to signed key and to signing key
                current_key = process_sig(pl, current_key)
                # Remember who signed whom
                keylist = process_signer(pl.id, current_key, keylist)
        else:
            pass

    if not args.allkeys:
        keylist = remove_unsigned(keylist)

    # output to dot goes here
    dot.create_dot(keylist, args.title, args.blackwhite, args.renderdate)


def remove_unsigned(keylist):

    ids = list(keylist.keys())
    for id in ids:
        if len(keylist[id].sigs) == 0:
            del keylist[id]

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

    if pl.id not in keylist:
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
    # if sigline.name == "[User ID not found]":
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
    if signer not in keylist:
        keylist[signer] = signer_key_dummy
    else:
        signer_key_dummy = keylist[signer]

    signer_key_dummy.addSigned(signed.id)

    keylist[signer_key_dummy.id] = signer_key_dummy

    return keylist


def getarg():
    """
    Parses command line parameters for known arguments.
    """

    usage = """
LANG=C gpg --no-options --with-colons --fixed-list-mode  --list-sigs
    --no-default-keyring --keyring ./myLUG.gpg | sig2dot > myLUG.dot"""

    parser = argparse.ArgumentParser(usage=usage)

    parser.add_argument("-a",
                        "--all-keys",
                        dest="allkeys",
                        action="store_true",
                        default=False,
                        help=_("Render all keys, even if they're not signed "
                               "by any other key."))

    parser.add_argument("-b",
                        "--black-white",
                        dest="blackwhite",
                        action="store_true",
                        default=False,
                        help="""Black and white / do not colourize. In fact,
                        it will be transparent. If you use this,
                        be sure not to use jpeg or other formats for graphing,
                        which do not support transparency.""")

    parser.add_argument("-d",
                        "--date",
                        dest="renderdate",
                        action="store",
                        default=datetime.utcnow().isoformat(),
                        help="""Render graph as it appeared on <date>
                        (ignores more recent signatures).
                        Date must be in the ISO8601 format.
                        UTC is assumed if zone designator is missing.
                        Will also ignore keys that have since been revoked.""")

    parser.add_argument("-q",
                        "--quiet",
                        dest="verbose",
                        action="store_false",
                        default=True,
                        help="Be quiet")

    parser.add_argument("-t",
                        "--title",
                        dest="title",
                        action="store",
                        default="unnamed",
                        help="Set title for graph. Default: unnamed.")

    parser.add_argument("-u",
                        "--user-not-found-string",
                        dest="user",
                        action="store",
                        default="[User ID not found]",
                        help="Set the [User ID not found]-String. See manpage"
                        " for Details.")

    parser.add_argument("-V",
                        "--version",
                        dest="version",
                        action="store_true",
                        default=False,
                        help="Show the current version.")

    args = parser.parse_args()

    check_args(args)

    return args


def check_args(args):

    if args.version is True:
        print("Version: 0.1.2")
        sys.exit(0)

    try:
        args.renderdate = iso8601.parse_date(args.renderdate)
    except iso8601.iso8601.ParseError:
        print("Please specify date in ISO8601 format.",
              file=sys.stderr)
        sys.exit(1)

    try:
        str(args.user)
    except:
        logger.error("Please specify a user-id-_STRING_.")
        sys.exit(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    main()
    sys.exit(0)
