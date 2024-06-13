{
    'name': 'Head Count Request',
    'version': '17.0.0.1',
    'category': 'Time Off',
    'sequence': -100,
    'summary': 'Head Count Request',
    'description': """Head Count Request""",
    'author': 'Loyal IT Solution',
    'website': 'https://www.loyalitsolutions.com',
    'depends': ['base', 'mail', 'hr', 'mrp'],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_inherit_view.xml',
        'views/template.xml',

    ],
    'installable': True,
    'auto_install': False,
}
