{
    'name': 'Invoice Multiple Sale Orders',
    'version': '1.0',
    'depends': ['base', 'sale_management'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',

        'views/multi_so_inv_views.xml',
        'views/so_order_line_views.xml',
        'views/menus.xml'
    ]
}