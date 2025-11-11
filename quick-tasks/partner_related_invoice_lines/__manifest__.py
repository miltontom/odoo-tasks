{
    "name": "Partner Related Invoice Lines",
    "depends": ["base", "contacts", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/related_invoice_line_views.xml",
        "views/account_move_views.xml",
    ],
}
