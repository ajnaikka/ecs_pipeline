# -*- coding: utf-8 -*-

{
    'name': 'Compensatory request',
    'version': '17.0.0.1',
    'category': 'Uncategorized',
    'sequence': -200,
    'summary': 'Compensatory request',
    'description': """Compensatory request""",
    'author': 'Loyal IT Solution',
    'website': 'https://www.loyalitsolutions.com',
    'depends': ['base','mail','hr','hr_attendance','hr_holidays','infinous_user_groups','portal','infi_portal_attendance_correction'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/email_wizard.xml',
        'wizards/shift_wizard.xml',
        'views/request.xml',
        'views/req_template.xml',
        'views/req_portal.xml',  
    ],
    'installable': True,
    'auto_install': False,
}