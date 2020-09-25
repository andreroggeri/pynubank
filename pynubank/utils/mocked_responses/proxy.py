proxy_login = {
    'access_token': 'access_token_123',
    'token_type': 'bearer',
    '_links': {
        'change_password': {'href': 'https://mocked-proxy-url/api/proxy/change_password_123'},
        'enabled_features': {'href': 'https://mocked-proxy-url/api/proxy/enabled_features_123'},
        'revoke_token': {'href': 'https://mocked-proxy-url/api/proxy/revoke_token_123'},
        'userinfo': {'href': 'https://mocked-proxy-url/api/proxy/userinfo_123'},
        'events_page': {'href': 'https://mocked-proxy-url/api/proxy/events_page_123'},
        'events': {'href': 'https://mocked-proxy-url/api/proxy/events_123'},
        'postcode': {'href': 'https://mocked-proxy-url/api/proxy/post_code_123'},
        'app_flows': {'href': 'https://mocked-proxy-url/api/proxy/app_flows_123'},
        'revoke_all': {'href': 'https://mocked-proxy-url/api/proxy/revoke_all_123'},
        'customer': {'href': 'https://mocked-proxy-url/api/proxy/customer_123'},
        'account': {'href': 'https://mocked-proxy-url/api/proxy/account_123'},
        'bills_summary': {'href': 'https://mocked-proxy-url/api/proxy/bills_summary_123'},
        'savings_account': {'href': 'https://mocked-proxy-url/api/proxy/savings_account_123'},
        'purchases': {'href': 'https://mocked-proxy-url/api/proxy/purchases_123'},
        'ghostflame': {'href': 'https://mocked-proxy-url/api/proxy/ghostflame_123'},
        'user_change_password': {'href': 'https://mocked-proxy-url/api/proxy/user_change_password_123'}
    }
}

proxy_lift = {
    'access_token': 'access_token_123',
    'token_type': 'bearer',
    '_links': {
        'change_password': {'href': 'https://mocked-proxy-url/api/proxy/change_password_123'},
        'enabled_features': {'href': 'https://mocked-proxy-url/api/proxy/enabled_features_123'},
        'revoke_token': {'href': 'https://mocked-proxy-url/api/proxy/revoke_token_123'},
        'userinfo': {'href': 'https://mocked-proxy-url/api/proxy/userinfo_123'},
        'events_page': {'href': 'https://mocked-proxy-url/api/proxy/events_page_123'},
        'events': {'href': 'https://mocked-proxy-url/api/proxy/events_123'},
        'postcode': {'href': 'https://mocked-proxy-url/api/proxy/post_code_123'},
        'app_flows': {'href': 'https://mocked-proxy-url/api/proxy/app_flows_123'},
        'revoke_all': {'href': 'https://mocked-proxy-url/api/proxy/revoke_all_123'},
        'customer': {'href': 'https://mocked-proxy-url/api/proxy/customer_123'},
        'account': {'href': 'https://mocked-proxy-url/api/proxy/account_123'},
        'bills_summary': {'href': 'https://mocked-proxy-url/api/proxy/bills_summary_123'},
        'savings_account': {'href': 'https://mocked-proxy-url/api/proxy/savings_account_123'},
        'purchases': {'href': 'https://mocked-proxy-url/api/proxy/purchases_123'},
        'ghostflame': {'href': 'https://mocked-proxy-url/api/proxy/ghostflame_123'},
        'user_change_password': {'href': 'https://mocked-proxy-url/api/proxy/user_change_password_123'}
    }
}

proxy_events = {
    'events': [{
        'description': 'Shopping Iguatemi', 'category': 'transaction', 'amount': 700,
        'time': '2017-09-09T02:03:55Z', 'title': 'transporte',
        'details': {'lat': -12.9818258, 'lon': -38.4652058, 'subcategory': 'card_present'},
        'id': 'abcde-fghi-jklmn-opqrst-uvxz',
        '_links': {'self': {'href': 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/_links_123'}},
        'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz'
    }],
    'as_of': '2017-09-09T06:50:22.323Z',
    'customer_id': 'abcde-fghi-jklmn-opqrst-uvxz',
    '_links': {
        'updates': {'href': 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/updates_123'},
        'next': {'href': 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/next_123'}
    }
}
