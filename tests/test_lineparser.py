import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sig2dot.gpg.colonimporter.LineParser
import sig2dot.gpg.colonimporter.PubLine
import sig2dot.gpg.colonimporter.SigLine
import sig2dot.gpg.colonimporter.UidLine

def test_parse_pub_line_with_expiry_date():
    _id = "ABCDEF0123456789"
    creation_date = "1514764800"
    expiry_date = "1577836800"

    line = f"pub:u:3072:1:{_id}:{creation_date}:{expiry_date}::u:::scESC::::::23::0:"

    result = sig2dot.gpg.colonimporter.LineParser.parse_line(line)

    assert isinstance(result, sig2dot.gpg.colonimporter.PubLine.PubLine)
    assert result.id == _id
    assert result.creationdate == creation_date
    assert result.expirydate == expiry_date

def test_parse_pub_line_without_expiry_date():
    _id = "ABCDEF0123456789"
    creation_date = "1514764800"

    line = f"pub:u:3072:1:{_id}:{creation_date}:::u:::scESC::::::23::0:"

    result = sig2dot.gpg.colonimporter.LineParser.parse_line(line)

    assert isinstance(result, sig2dot.gpg.colonimporter.PubLine.PubLine)
    assert result.id == _id
    assert result.creationdate == creation_date
    assert result.expirydate == -1

def test_parse_sig_line_with_expiry():
    _id = "ABCDEF0123456789"
    sign_date = "1514764800"
    expiry_date = "1577836800"
    name = "Bob Example <bob@example.com>"

    line = f"sig:::1:{_id}:{sign_date}:{expiry_date}:::{name}:13x:::::10:"

    result = sig2dot.gpg.colonimporter.LineParser.parse_line(line)

    assert isinstance(result, sig2dot.gpg.colonimporter.SigLine.SigLine)
    assert result.id == _id
    assert result.signdate == sign_date
    assert result.expirydate == expiry_date
    assert result.name == name

def test_parse_sig_line_without_expiry():
    _id = "ABCDEF0123456789"
    sign_date = "1514764800"
    name = "Bob Example <bob@example.com>"

    line = f"sig:::1:{_id}:{sign_date}::::{name}:13x:::::10:"

    result = sig2dot.gpg.colonimporter.LineParser.parse_line(line)

    assert isinstance(result, sig2dot.gpg.colonimporter.SigLine.SigLine)
    assert result.id == _id
    assert result.signdate == sign_date
    assert result.expirydate == -1
    assert result.name == name

def test_parse_uid_line_with_comment():
    name = "Bob Example"
    comment = "Example Inc"
    email = "bob@example.com"

    line = f"uid:u::::1514764800::ABCDEABCDEABCDEABCDE01234567890123456789::{name} ({comment}) <{email}>::::::::::0:"

    result = sig2dot.gpg.colonimporter.LineParser.parse_line(line)

    assert isinstance(result, sig2dot.gpg.colonimporter.UidLine.UidLine)
    assert result.name == name
    assert result.comment == comment
    assert result.email == email

def test_parse_uid_line_without_comment():
    name = "Bob Example"
    email = "bob@example.com"

    line = f"uid:u::::1514764800::ABCDEABCDEABCDEABCDE01234567890123456789::{name} <{email}>::::::::::0:"

    result = sig2dot.gpg.colonimporter.LineParser.parse_line(line)

    assert isinstance(result, sig2dot.gpg.colonimporter.UidLine.UidLine)
    assert result.name == name
    assert result.comment == ""
    assert result.email == email
