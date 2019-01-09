import setuptools

with open("README.md") as f:
    long_description = f.read()

requires = [
    "iso8601",
]

setuptools.setup(
    name="sig2dot",
    version="0.1.2",
    author="Benjamin Marwell",
    author_email="e-post@bmarwell.de",
    description="Parses gpg-signature-output and creates a dot-file for graphviz",
    entry_points={
        "console_scripts": [
            "sig2dot=sig2dot.sig2dot:main",
        ]
    },
    install_requires=requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bmhm/sig2dot2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
