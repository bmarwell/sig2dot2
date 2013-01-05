#!/bin/bash
keyring="./A.keyring"
trustdb="/tmp/trustdb.sig2dot.test1"
gpgopt=" --no-options --no-default-keyring --keyring $keyring --trustdb-name $trustdb  "
RETURN=0
outfile="test1.dot"
pgpkeyfp="FFDDF8BFB0D2F44D"
pgpkeyname="sig2dot2 test1 A"
pgpcolourout="\/\/0.0::0.833::0.333\/\/"

TESTOUT=$(gpg $gpgopt $QUIET --with-colons --fixed-list-mode --list-sigs | ../../sig2dot/sig2dot.py -u "[User-ID nicht gefunden]" > "$outfile"; echo $?)
RC=$(echo "$TESTOUT" | tail -n 1)
if [ "x$RC" != "x0" ]; then
    echo "failed"
    RETURN=1
fi


# check if the dot file has been produced
if [ ! -f "$outfile" ]; then
    echo "no outfile produced"
    RETURN=1
fi

# check if the output is as expected
colourline=$(grep "${pgpkeyfp}.*label=\"${pgpkeyname}\".*${pgpcolourout}" "$outfile")
if [ -z "${colourline}" ]; then
    echo "not correct colours found or line not existent"
    RETURN=1
fi

echo -e "TEST RESULTS:\n$TESTOUT"

# leave outfile, if test failed
if [ "x$RC" == "x0" ]; then
    rm "$outfile"
fi

# return code for git filter etc.
exit $RETURN
