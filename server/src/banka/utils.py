import json

from forge.redis import r


BANKA_SESSION_TOKEN_KEY = 'banka_session_token'
BANKA_CARDS_KEY = 'banka_cards'


def get_session_token():
    return r.get(BANKA_SESSION_TOKEN_KEY)


def set_session_token(token):
    r.setex(BANKA_SESSION_TOKEN_KEY, 60 * 5, token)


def get_balance():
    cards = json.loads(r.get(BANKA_CARDS_KEY))
    balance_sum = sum(c.get('balance') for c in cards)
    balance_repr = str(int(int(balance_sum) / 100))
    return balance_repr


def set_cards(cards):
    r.set(BANKA_CARDS_KEY, json.dumps(cards))
