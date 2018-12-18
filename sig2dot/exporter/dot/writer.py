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

import logging
import sys

from colorsys import rgb_to_hsv
from calendar import timegm

from gpg import OpenPGPKey, OpenPGPSig

logger = logging.getLogger(__name__)


# =============================================================================
# Main function
# =============================================================================
def create_dot(keylist, title, trans, date):
    """

    @param keylist:   OpenPGP-Keys
    @type keylist:    list(OpenPGPKey)
    @param title:     tile of the graph
    @type title:      string
    @param trans:     Wether bw/transparency is desired
    @type trans:      boolean
    @param date:      Date in YYYY-MM-DD for which the graph should be rend.
    @type date:       string (YYYY-MM-DD)
    """

    unixtime = int(date.timestamp())

    logger.info("Renderdate: %s (%d)" % (date.isoformat(), unixtime))

    # Calculate maximums for colouring
    max_sigs = get_max_sigs(keylist)
    max_signed = get_max_signed(keylist)
    max_ratio = get_max_sigratio(keylist)

    # now write selected keys
    write_header(title)
    write_keys(keylist, max_sigs, max_signed, max_ratio, trans)
    write_relations(keylist, unixtime)
    write_footer()


# ==============================================================================
# Helper functions for other functions
# ==============================================================================

def get_relations(keylist, unixtime):

    relationlist = list()

    for key in keylist.values():
        # Format: "id" -> "id"
        for signer in key.sigs:

            # Also make sure we do not draw revoked sigs
            draw = True
            if (int(signer.expirydate) < unixtime) \
                    and (int(signer.expirydate) != -1):
                draw = False
            # Signatures which didn't exist yet.
            if int(signer.signdate) > unixtime:
                draw = False

            if draw == True:
                relationlist.append("""    \"{0}\"    ->    \"{1}\""""
                                    .format(signer.id,    key.id)
                                    )
            else:
                # revoked or hasn't been signed on <unixtime>
                pass

    return set(relationlist)


# =============================================================================
# Calculate some maximums for colouring
# =============================================================================
def get_max_sigratio(keylist):

    # again:
    #    signed  = given signatures
    #    sigs    = gotten signatures
    # ratio =  given / gotten
    max_keyratio = 0
    for id, key in keylist.items():
        # print("Signed:", len(key.signed))
        # print("Gotten:", len(key.sigs))
        if ((len(key.signed) > 0) and (len(key.sigs) > 0)):
            if (len(key.signed) / len(key.sigs)) > max_keyratio:
                max_keyratio = (len(key.signed) / len(key.sigs))

    logger.info("Max_Ratio: %s" % max_keyratio)

    return max_keyratio


def get_max_signed(keylist):

    max_signed = 0
    for key in keylist.values():
        if len(key.signed) > max_signed:
            max_signed = len(key.signed)

    return max_signed


def get_max_sigs(keylist):

    max_sigs = 0
    for key in keylist.values():
        if len(key.sigs) > max_sigs:
            max_sigs = len(key.sigs)

    return max_sigs


# =============================================================================
# Output related functions
# =============================================================================
def write_header(title):

    print("digraph \"" + title + "\" {")
    print("""    
    overlap=scale
    splines=true
    sep=.1
    bgcolor=transparent
    node [style=filled]
    """)


def write_keys(keylist, max_sigs, max_signed, max_ratio, trans):

    red, green, blue = (0, 1/3, 1/3)

    # Format:
    # "ID"    [fillcolor="h,s,v",label="key.name"]
    # =========================================================================
    # FIX: I'm not sure if I mixed up signed vs sigs. Can anyone help?
    # =========================================================================

    for key in keylist.values():
        red = len(key.signed) / max_signed
        green = (len(key.sigs) / len(key.signed) / max_ratio * 0.75) * 2/3 + 1/3
        blue = (len(key.sigs) / max_sigs) * 2/3 + 1/3

        h, s, v = rgb_to_hsv(red, green, blue)
        print("""    \"{0}\"  [label="{1}" """
              .format(key.id, key.name),
              end="")

        if trans == True:
            print(""",fillcolor="transparent" """)
        else:
            print(""",fillcolor="{0},{1},{2}" """
                  .format(h, s, v), end=""
                  )

        print("]")


def write_relations(keylist, unixtime):

    # unfortunately, we need to store everything, so we can
    # remove double entries
    relationlist = get_relations(keylist, unixtime)

    for rel in relationlist:
        print(rel)


def write_footer():

    print("}")
