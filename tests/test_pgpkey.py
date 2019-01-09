import sig2dot.gpg.OpenPGPKey

def test_blank_key():
    result = sig2dot.gpg.OpenPGPKey.OpenPGPKey()

    assert result.id == ""
    assert result.creationdate == 0
    assert result.expirydate == 0
    assert result.name == ""
    assert result.comment == ""
    assert result.email == ""
    assert not result.sigs
    assert not result.signed

def test_key_properties():
    _id = "ABCDEF0123456789"
    creation_date = "1514764800"
    expiry_date = "1577836800"
    name = "Bob Example"
    comment = "Example Inc"
    email = "bob@example.com"

    result = sig2dot.gpg.OpenPGPKey.OpenPGPKey()
    result.id = _id
    result.creationdate = creation_date
    result.expirydate = expiry_date
    result.name = name
    result.comment = comment
    result.email = email

    assert result.id == _id
    assert result.creationdate == creation_date
    assert result.expirydate == expiry_date
    assert result.name == name
    assert result.comment == comment
    assert result.email == email
