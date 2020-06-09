import pytest


@pytest.fixture
def authentication_return():
    return {
        "access_token": "access_token_123",
        "token_type": "bearer",
        "_links": {
            "change_password": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/change_password_123"
            },
            "enabled_features": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/enabled_features_123"
            },
            "revoke_token": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/revoke_token_123"
            },
            "userinfo": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/userinfo_123"
            },
            "events_page": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/events_page_123"
            },
            "events": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/events_123"
            },
            "postcode": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/post_code_123"
            },
            "app_flows": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/app_flows_123"
            },
            "revoke_all": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/revoke_all_123"
            },
            "customer": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/customer_123"
            },
            "account": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/account_123"
            },
            "bills_summary": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/bills_summary_123"
            },
            "savings_account": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/savings_account_123"
            },
            "purchases": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/purchases_123"
            },
            "ghostflame": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/ghostflame_123"
            },
            "user_change_password": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/user_change_password_123"
            }
        },
    }
