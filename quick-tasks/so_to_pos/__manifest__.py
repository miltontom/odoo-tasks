{
    "name": "POS Order From Sale Order",
    "depends": ["sale_management", "point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/make_pos_order_views.xml",
        "views/payment_line_views.xml",
        "views/sale_order_views.xml",
    ],
}
