# -*- coding: utf-8 -*-

{
    'name': 'Approval User Group',
    'version': '17.0.0.1',
    'category': 'Uncategorized',
    'sequence': -100,
    'summary': 'Approval User Group',
    'description': """Approval User Group for different approvals""",
    'author': 'Loyal IT Solution',
    'website': 'https://www.loyalitsolutions.com',
    'depends': ['base','hr','hr_contract','hr_payroll','hr_work_entry_contract_attendance','hr_holidays'],
    'data': [

        'security/security.xml',
        'views/contract.xml',
        'views/template.xml',


    ],
    'installable': True,
    'auto_install': False,
}
