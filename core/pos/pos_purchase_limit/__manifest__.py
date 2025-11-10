{
    "name": "POS Purchase Limit",
    "version": "0.1.0",
    "author": "Milton Tom",
    "depends": ["base", "point_of_sale", "contacts"],
    "installable": True,
    "data": [
        "views/res_partner_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_purchase_limit/static/src/js/pos_store.js",
            "pos_purchase_limit/static/src/js/popup.js",
            "pos_purchase_limit/static/src/xml/popup.xml",
        ]
    }
}
