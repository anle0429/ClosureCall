from scripts.check_secrets import check

def test_scanner_detects_values_and_keys_without_matching_its_own_patterns():
    assert check(b'synthetic-configured-secret',['synthetic-configured-secret'])
    header=b'-----BEGIN '+b'OPENSSH PRIVATE KEY-----'
    assert not check(header,[])
    assert check(header+b'\n'+b'A'*100+b'\n',[])
