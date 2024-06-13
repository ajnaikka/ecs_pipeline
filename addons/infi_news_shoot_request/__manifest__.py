# -*- coding: utf-8 -*-

{
    'name': 'Shoot Request',
    'version': '17.0.0.1',
    'category': 'Uncategorized',
    'sequence': -100,
    'summary': 'Approval User Group',
    'description': """Approval User Group for different approvals""",
    'author': 'Loyal IT Solution',
    'website': 'https://www.loyalitsolutions.com',
    'depends': ['base','mail','stock','hr','mrp','infinous_user_groups'],
    'data': [

        'security/ir.model.access.csv',
        'wizard/mail_compose_wizard.xml',
        'views/shoot_request.xml',
        'views/template.xml',
        'views/kit.xml',


    ],
    'installable': True,
    'auto_install': False,
}