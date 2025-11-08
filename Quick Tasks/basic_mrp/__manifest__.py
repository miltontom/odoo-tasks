{
    "name": "Basic MRP",
    "depends": ["base", "stock", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "data/basic_mrp.xml",
        "views/basic_mrp_views.xml",
        "views/basic_mrp_component_views.xml",
        "views/basic_bom_views.xml",
        "views/basic_bom_component_views.xml",
        "views/basic_mrp_menus.xml",
    ],
    "assets": {"web.assets_backend": ["basic_mrp/static/src/**/*"]},
}
