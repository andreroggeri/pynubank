import fnmatch
from pynubank.utils.http import HttpClient
from pynubank.utils.graphql import prepare_request_body
from pynubank import NuException

from pynubank.utils.mocked_responses import discovery
from pynubank.utils.mocked_responses import proxy
from pynubank.utils.mocked_responses import bills
from pynubank.utils.mocked_responses import account
from pynubank.utils.mocked_responses import money
from pynubank.utils.mocked_responses import boleto


class MockHttpClient(HttpClient):
    def get(self, url: str) -> dict:
        result = self._find(url)
        if result is None:
            raise NuException(f'There is no result expected for {url}')
        return result

    def post(self, url: str, json: dict) -> dict:
        result = self._find(url, json)
        if result is None:
            json['variables'] = {}
            result = self._find(url, json)

            if result is None:
                raise NuException(f'There is no result expected for {url}')
        return result

    def _find(self, url: str, json: dict = None):
        result = self._results.get((url, ''))
        if result:
            return result

        params = '' if json is None else str(json)
        for k in self._results.keys():
            if fnmatch.fnmatch(url, k[0]):
                return self._results.get((k[0], params))

    _results = {}
    _results[('https://*/api/discovery', '')] = discovery.api_discovery
    _results[('https://*/api/app/discovery', '')] = discovery.app_discovery
    _results[('https://mocked-proxy-url/api/token', '')] = discovery.login
    _results[('https://mocked-proxy-url/api/proxy/login', '')] = discovery.login
    _results[('https://mocked-proxy-url/api/proxy/lift', '')] = discovery.login

    _results[('https://mocked-proxy-url/api/proxy/bills_summary_123', '')] = bills.bills_summary
    _results[('https://mocked-proxy-url/api/proxy/events_123', '')] = proxy.proxy_events

    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
              str(prepare_request_body('account_balance')))] = account.account_balance
    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
              str(prepare_request_body('account_feed')))] = account.feed
    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
              str(prepare_request_body('account_investments')))] = account.investments

    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
              str(prepare_request_body('account_id')))] = boleto.create
    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
              str(prepare_request_body('create_boleto')))] = boleto.create

    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
              str(prepare_request_body('create_money_request')))] = money.request

    _results[('https://*/api/bills/*', '')] = bills.bills
