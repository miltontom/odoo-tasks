{
    "name": "MultiSafepay Integration",
    "author": "Milton Tom",
    'category': 'Accounting/Payment Providers',
    "depends": ["base", "payment"],
    "data": [
        "data/payment_provider_data.xml",

        "views/payment_provider_views.xml",
        "views/payment_multisafepay_templates.xml",
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_multisafepay/static/src/**/*',
        ],
    },
}