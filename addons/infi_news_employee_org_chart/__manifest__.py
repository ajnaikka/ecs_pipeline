# -*- coding: utf-8 -*-

{
    'name': 'Employee Org Chart',
    'version': '17.0.0.1',
    'category': 'Uncategorized',
    'sequence': -100,
    'summary': 'Employee Org Chart',
    'description': """Employee Org Chart""",
    'author': 'Loyal IT Solution',
    'website': 'https://www.loyalitsolutions.com',
    'depends': ['base', 'mail', 'stock', 'hr','hr_org_chart', 'hr_payroll'],
    'data': [
        'views/hr_emloyee_public_inherit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
