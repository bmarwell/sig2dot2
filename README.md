# sig2dot2

A revised version of sig2dot (creating PGP signing web-of-trust-graphics) written in python.

## REQUIREMENTS
sig2dot (revised) uses python3. If you do not have python3 installed,
get it at: http://www.python.org/.

If you're using Debian/Ubuntu or any other .deb-based Distribution, you can
most likely just type:
```$ sudo aptitude install python3```

The most important application is gnupg. Without it, you are unable to feed
sig2dot with data.
```$ sudo aptitude install gnupg gpg```
    
Also, for converting the dot-file to any other format, you need one of:  
    ```[dot, neato, fdp, circo, twopi]```

They can be found in the graphviz-package.
```$ sudo aptitude install graphviz```

## USAGE/INVOCATION
Have a keyring ready and feed sig2dot with its signatures:
```
$ gpg --no-options --with-colons --fixed-list-mode  --list-sigs \
    --no-default-keyring --keyring ./myLUG.gpg |                \
    ./sig2dot.py -u "[User ID not found]" > myLUG.dot
```
Then convert it using neato:
```$ neato -Tpng myLUG.dot > myLUG.png```
