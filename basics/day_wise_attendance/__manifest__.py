{
    'name': 'Day Wise Attendance',
    'version': '0.1.0',
    'author': 'Milton Tom',
    'depends': ['base', 'hr_attendance'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',

        'data/actions.xml',

        'views/attendance_views.xml',
        'views/menus.xml'
    ]
}