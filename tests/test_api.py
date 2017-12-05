from nose.tools import eq_, ok_
from nose.tools import assert_not_equal
import app
import json

app.testing = True
client = app.app.test_client()

def test_get_index():
    res = client.get('/')
    eq_(200, res.status_code)

def test_get_weblio():
    res = client.get('/weblio/')
    assert_not_equal(200, res.status_code)

    res = client.get('/weblio/en/')
    assert_not_equal(200, res.status_code)

    res = client.get('/weblio/en/bad/')
    assert_not_equal(200, res.status_code)

    res = client.get('/weblio/en/en/')
    assert_not_equal(200, res.status_code)

    res = client.get('/weblio/en/ja/')
    eq_(200, res.status_code)

def test_right_return_weblio():
    res = client.get('/weblio/en/ja/?text=I have a pen.')
    result = json.loads(res.data)
    ok_(isinstance(result, list))

    res = client.get('/weblio/ja/en/?text=私はペンを持っている．')
    result = json.loads(res.data)
    ok_(isinstance(result, list))

def test_get_excite():
    res = client.get('/excite/')
    assert_not_equal(200, res.status_code)

    res = client.get('/excite/en/')
    assert_not_equal(200, res.status_code)

    res = client.get('/excite/en/bad/')
    assert_not_equal(200, res.status_code)

    res = client.get('/excite/en/en/')
    assert_not_equal(200, res.status_code)

    res = client.get('/excite/en/ja/')
    eq_(200, res.status_code)

def test_right_return_excite():
    res = client.get('/excite/en/ja/?text=I have a pen.')
    result = json.loads(res.data)
    ok_(isinstance(result, list))

    res = client.get('/excite/ja/en/?text=私はペンを持っている．')
    result = json.loads(res.data)
    ok_(isinstance(result, list))
