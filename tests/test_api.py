from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_company_refresh_and_fetch():
    r = client.post('/company/aapl/refresh')
    assert r.status_code == 200
    r2 = client.get('/company/AAPL/facts')
    assert r2.status_code == 200
    assert r2.json()['ticker'] == 'AAPL'


def test_trade_and_review():
    tr = client.post('/trades', json={
        'ticker': 'msft',
        'strategy': 'long_call',
        'direction': 'bullish',
        'thesis': 'learning thesis',
        'risk_plan': 'max loss premium',
        'invalidation': 'break below support',
        'entry_trigger': 'close above resistance'
    })
    assert tr.status_code == 200
    trade_id = tr.json()['id']

    rv = client.post('/reviews', json={'trade_id': trade_id, 'outcome': 'win', 'lessons': 'followed plan'})
    assert rv.status_code == 200
