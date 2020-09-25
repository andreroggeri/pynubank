def api_discovery():
    return {
        'register_prospect_savings_web': 'https://mocked-proxy-url/api/proxy/register_prospect_savings_web',
        'register_prospect_savings_mgm': 'https://mocked-proxy-url/api/proxy/register_prospect_savings_mgm',
        'pusher_auth_channel': 'https://mocked-proxy-url/api/proxy/pusher_auth_channel',
        'register_prospect_debit': 'https://mocked-proxy-url/api/proxy/register_prospect_debit',
        'reset_password': 'https://mocked-proxy-url/api/proxy/reset_password',
        'register_prospect': 'https://mocked-proxy-url/api/proxy/register_prospect',
        'register_prospect_savings_request_money': 'https://mocked-proxy-url/api/proxy/register_prospect_savings_request_money',
        'register_prospect_global_web': 'https://mocked-proxy-url/api/proxy/register_prospect_global_web',
        'register_prospect_c': 'https://mocked-proxy-url/api/proxy/register_prospect_c',
        'request_password_reset': 'https://mocked-proxy-url/api/proxy/request_password_reset',
        'auth_gen_certificates': 'https://mocked-proxy-url/api/proxy/auth_gen_certificates',
        'login': 'https://mocked-proxy-url/api/proxy/login',
        'email_verify': 'https://mocked-proxy-url/api/proxy/email_verify',
        'auth_device_resend_code': 'https://mocked-proxy-url/api/proxy/auth_device_resend_code',
        'msat': 'https://mocked-proxy-url/api/proxy/msat'
    }


def app_discovery():
    return {
        'scopes': 'https://mocked-proxy-url/api/admin/scope',
        'creation': 'https://mocked-proxy-url/api/creation',
        'change_password': 'https://mocked-proxy-url/api/change-password',
        'smokejumper': 'https://prod-cdn.nubank.com.br/mobile/fire-station/smokejumper.json',
        'block': 'https://mocked-proxy-url/api/admin/block',
        'lift': 'https://mocked-proxy-url/api/proxy/lift',
        'shard_mapping_id': 'https://mocked-proxy-url/api/mapping/:kind/:id',
        'force_reset_password': 'https://mocked-proxy-url/api/admin/force-reset-password',
        'revoke_token': 'https://mocked-proxy-url/api/proxy/revoke_token',
        'userinfo': 'https://mocked-proxy-url/api/userinfo',
        'reset_password': 'https://mocked-proxy-url/api/proxy/reset_password',
        'unblock': 'https://mocked-proxy-url/api/admin/unblock',
        'shard_mapping_cnpj': 'https://mocked-proxy-url/api/proxy/shard_mapping_cnpj',
        'shard_mapping_cpf': 'https://mocked-proxy-url/api/mapping/shard_mapping_cpf',
        'register_prospect': 'https://mocked-proxy-url/api/proxy/register_prospect',
        'engage': 'https://mocked-proxy-url/api/proxy/engage',
        'account_recovery_job': 'https://mocked-proxy-url/api/proxy/account_recovery_job',
        'account_recovery_confirm': 'https://mocked-proxy-url/api/proxy/account_recovery_confirm',
        'magnitude': 'https://prod-s0-magnitude.nubank.com.br/api/events',
        'revoke_all': 'https://mocked-proxy-url/api/proxy/revoke_all',
        'user_hypermedia': 'https://mocked-proxy-url/api/admin/users/:id/hypermedia',
        'gen_certificate': 'https://mocked-proxy-url/api/proxy/gen_certificate',
        'email_verify': 'https://mocked-proxy-url/api/proxy/email_verify',
        'prospect_location': 'https://mocked-proxy-url/api/proxy/prospect_location',
        'token': 'https://mocked-proxy-url/api/token',
        'account_recovery': 'https://mocked-proxy-url/api/proxy/account_recovery',
        'start_screen_v2': 'https://mocked-proxy-url/api/proxy/start_screen_v2',
        'scopes_remove': 'https://mocked-proxy-url/api/admin/scope/:admin-id',
        'approved_products': 'https://mocked-proxy-url/api/proxy/approved_products',
        'admin_revoke_all': 'https://mocked-proxy-url/api/proxy/admin_revoke_all',
        'faq': {'ios': 'https://ajuda.nubank.com.br/ios', 'android': 'https://ajuda.nubank.com.br/android',
                'wp': 'https://ajuda.nubank.com.br/windows-phone'},
        'scopes_add': 'https://mocked-proxy-url/api/admin/scope/:admin-id',
        'registration': 'https://mocked-proxy-url/api/proxy/registration',
        'global_services': 'https://mocked-proxy-url/api/mapping/global-services',
        'start_screen': 'https://mocked-proxy-url/api/proxy/start_screen',
        'user_change_password': 'https://mocked-proxy-url/api/user/:user-id/password',
        'account_recovery_token': 'https://mocked-proxy-url/api/proxy/account_recovery_token',
        'user_status': 'https://mocked-proxy-url/api/admin/user-status',
        'engage_and_create_credentials': 'https://mocked-proxy-url/api/proxy/engage_and_create_credentials'
    }


def login():
    return {
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
