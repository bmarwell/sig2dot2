#!/bin/bash
keyring="./A.keyring"
trustdb="/tmp/trustdb.sig2dot.test1"
gpgopt=" --no-options --no-default-keyring --keyring $keyring --trustdb-name $trustdb  "
RETURN=0

TESTOUT=$(gpg $gpgopt $QUIET --with-colons --fixed-list-mode --list-sigs | ../../sig2dot/sig2dot.py -u "[User-ID nicht gefunden]" > test1.dot; echo $?)
RC=$(echo "$TESTOUT" | tail -n 1)
if [ "x$RC" != "x0" ]; then
    echo "failed"
    RETURN=1
fi

echo -e "TEST RESULTS:\n$TESTOUT"
exit $RETURN
