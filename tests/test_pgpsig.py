import sig2dot.gpg.OpenPGPSig

def test_blank_sig():
    result = sig2dot.gpg.OpenPGPSig.OpenPGPSig()

    assert result.id == ""
    assert result.signdate == -1
    assert result.expirydate == -1

def test_sig_properties():
    _id = "ABCDEF0123456789"
    sign_date = "1514764800"
    expiry_date = "1577836800"

    result = sig2dot.gpg.OpenPGPSig.OpenPGPSig()
    result.id = _id
    result.signdate = sign_date
    result.expirydate = expiry_date

    assert result.id == _id
    assert result.signdate == sign_date
    assert result.expirydate == expiry_date
