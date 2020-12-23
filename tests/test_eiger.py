from backend.eiger import EigerModule


def test_construct_module():
    m = EigerModule()
    assert m['id'] == None


def test_load_module_that_does_not_exist():
    m = EigerModule()
    m.load('T4567')
    assert m['id'] == None


def test_load_module():
    m = EigerModule()
    m.load('T22')
    assert m['id'] == 'T22'
    assert m['beb_top']['id'] == '18_14_00061'
    assert m['beb_bot']['id'] == '18_14_00099'
    assert m['feb_top']['id'] == '08_15_00061'
    assert m['feb_bot']['id'] == '08_15_00060'

def test_iterate_empty_module():
    m = EigerModule()
    default_keys = ['id', 'feb_bot', 'feb_top', 'beb_bot', 'beb_top', 'extra']
    for key, value in m.items():
        assert key in default_keys
        if key != 'extra':
            assert value == None

def test_load_using_none():
    m = EigerModule()
    m.load(None)
    assert m['id'] == None



