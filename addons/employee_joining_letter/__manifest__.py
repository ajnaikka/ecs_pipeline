# -*- coding: utf-8 -*-

{
    'name': 'Employee Joining Letter',
    'version': '17.0.0.1',
    'category': 'Employee',
    'sequence': -100,
    'summary': 'Employee Joining Letter Creation',
    'description': """Employee Joining Letter Creation""",
    'author': 'Loyal IT Solution',
    'website': 'https://www.loyalitsolutions.com',
    'depends': ['base','mail','hr','infinous_user_groups'],
    'data': [

        'security/ir.model.access.csv',
        'report/joining_letter_pdf_format.xml',
        'report/joining_letter_pdf_template.xml',
        'views/emp_joining_letter.xml',
    ],
    'installable': True,
    'auto_install': False,
}