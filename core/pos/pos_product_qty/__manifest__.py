{
    "name": "POS Extended",
    "version": "0.1.0",
    "author": "Milton Tom",
    "depends": ["base", "point_of_sale"],
    "installable": True,
    "data": ["views/res_config_settings_views.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_ext/static/src/product_card.js",
            "pos_ext/static/src/product_card.xml",
            "pos_ext/static/src/product_screen.xml",
        ]
    },
}
