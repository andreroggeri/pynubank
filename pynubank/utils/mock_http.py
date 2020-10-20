import os
import json
import fnmatch
from pathlib import Path
from pynubank.utils.http import HttpClient
from pynubank.utils.graphql import prepare_request_body
from pynubank import NuException


class MockHttpClient(HttpClient):
    _results = {}

    def __init__(self, test_new_feed_bills_urls: bool = False):
        super().__init__()
        self._results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
                       str(prepare_request_body('account_balance')))] = self._read_data('account_balance')
        self._results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
                       str(prepare_request_body('account_feed')))] = self._read_data('account_feed')
        self._results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
                       str(prepare_request_body('account_investments')))] = self._read_data('account_investments')
        self._results[('https://*/api*bills/*', '')] = self._read_data('bills')
        self._results[('https://mocked-proxy-url/api/proxy/bills_summary_123', '')] = self._read_data('bills_summary')
        self._results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
                       str(prepare_request_body('account_id')))] = self._read_data('boleto_create')
        self._results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
                       str(prepare_request_body('create_boleto')))] = self._read_data('boleto_create')
        self._results[('https://*/api/discovery', '')] = self._read_data('discovery_api')
        self._results[('https://*/api/app/discovery', '')] = self._read_data('discovery_app')
        self._results[('https://mocked-proxy-url/api/token', '')] = self._read_data('discovery_login',
                                                                                    test_new_feed_bills_urls=test_new_feed_bills_urls)
        self._results[('https://mocked-proxy-url/api/proxy/login', '')] = self._read_data('discovery_login',
                                                                                          test_new_feed_bills_urls=test_new_feed_bills_urls)
        self._results[('https://mocked-proxy-url/api/proxy/lift', '')] = self._read_data('discovery_login',
                                                                                         test_new_feed_bills_urls=test_new_feed_bills_urls)
        self._results[('https://mocked-proxy-url/api/proxy/events_123', '')] = self._read_data('proxy_events')
        self._results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
                       str(prepare_request_body('create_money_request')))] = self._read_data('money')

        if test_new_feed_bills_urls:
            self._results[('https://mocked-proxy-url/api/proxy/magnitude_123', '')] = self._read_data('proxy_events')
            self._results[('https://mocked-proxy-url/api/proxy/savings_account_123', '')] = self._read_data(
                'bills_summary')
        else:
            self._results[('https://mocked-proxy-url/api/proxy/events_123', '')] = self._read_data('proxy_events')
            self._results[('https://mocked-proxy-url/api/proxy/bills_summary_123', '')] = self._read_data(
                'bills_summary')

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

    @staticmethod
    def _read_data(name: str, test_new_feed_bills_urls: bool = False) -> dict:
        json_path = Path(__file__).parent.joinpath('mocked_responses', f'{name}.json').absolute()
        json_dictionary = json.loads(open(json_path, 'r').read())
        if name == "discovery_login":
            if test_new_feed_bills_urls:
                json_dictionary["_links"]["magnitude"] = {
                    "href": "https://mocked-proxy-url/api/proxy/magnitude_123"
                }
                json_dictionary["_links"]["savings_account"] = {
                    "href": "https://mocked-proxy-url/api/proxy/savings_account_123"
                }
            else:
                json_dictionary["_links"]["events"] = {
                    "href": "https://mocked-proxy-url/api/proxy/events_123"
                }
                json_dictionary["_links"]["bills_summary"] = {
                    "href": "https://mocked-proxy-url/api/proxy/bills_summary_123"
                }
        return json_dictionary
