# sig2dot2

A revised version of sig2dot (creating PGP signing web-of-trust-graphics) written in python.

## REQUIREMENTS

sig2dot (revised) uses python >= 3.3. If you do not have python3 installed,
get it at: http://www.python.org/.

If you're using Debian/Ubuntu or any other .deb-based Distribution, you can
most likely just type:
```
$ sudo apt install python3
```

Clone the repo, and install with pip(3):
```
$ git clone https://github.com/bmhm/sig2dot2.git
$ pip3 install --user sig2dot2
```

The most important application is gnupg. Without it, you are unable to feed
sig2dot with data.
```
$ sudo apt install gnupg gpg
```
    
Also, for converting the dot-file to any other format, you need one of:  
```
[dot, neato, fdp, circo, twopi]
```

They can be found in the graphviz-package.
```
$ sudo apt install graphviz
```

## USAGE/INVOCATION

Have a keyring ready and feed sig2dot with its signatures. The setup has
provided "sig2dot" as a command line utility.
```
$ gpg --no-options --with-colons --fixed-list-mode  --list-sigs \
    --no-default-keyring --keyring ./myLUG.gpg |                \
    sig2dot -u "[User ID not found]" > myLUG.dot
```

Then convert it using neato:
```
$ neato -Tpng myLUG.dot > myLUG.png
```

## CONTRIBUTING

Testing is done with pytest via tox:
```
$ pip3 install --user tox
$ tox
```
