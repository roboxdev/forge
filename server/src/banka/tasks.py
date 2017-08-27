import requests
from celery import shared_task
from celery.utils.log import get_logger
from django.conf import settings

from .utils import set_cards, set_session_token, get_session_token, renew_token_ttl

logger = get_logger(__name__)

SESSION_EXPIRED_ERROR = 'SESSION_EXPIRED_OR_CLOSED'
SYSTEM_ERROR = 'SYSTEM_ERROR'


@shared_task(bind=True)
def fetch_and_save_cards_task(self, force_auth=False):
    session_token = get_session_token()
    logger.debug('force_auth: %s; session_token: %s', force_auth, session_token)
    if force_auth or not session_token:
        auth_response = requests.post(
            url='https://24.bankastana.kz/BankAstanaApi/v1/auth/auth_by_login',
            data={
                'login': settings.BANKASTANA_LOGIN,
                'password': settings.BANKASTANA_PASSWORD,
                'clientInfo': '{}',
            },
        ).json()
        logger.info('auth_by_login response: %s', auth_response)
        auth_response_data = auth_response['data']
        session_token = auth_response_data['reference']
        set_session_token(session_token)

    accounts_response = requests.post(
        url='https://24.bankastana.kz/BankAstanaApi/v1/accounts/get_accounts',
        data={
            'session': session_token,
        },
    ).json()
    logger.info('get_accounts response: %s', accounts_response)
    status = accounts_response.get('status')
    if status == 'error':
        error_code = accounts_response.get('error_code')
        if error_code == SESSION_EXPIRED_ERROR:
            logger.info('Session expired. Retrying...')
            self.retry(kwargs={'force_auth': True}, countdown=1)
        elif error_code == SYSTEM_ERROR:
            logger.warning('SYSTEM_ERROR. retrying in 1 hr')
            self.retry(kwargs={'force_auth': True}, countdown=60 * 60)
        else:
            logger.error('Unknown error_code: %s', error_code)
    elif status == 'success':
        renew_token_ttl()
        accounts_response_data = accounts_response.get('data')
        cards = accounts_response_data.get('cards')
        set_cards(cards)

