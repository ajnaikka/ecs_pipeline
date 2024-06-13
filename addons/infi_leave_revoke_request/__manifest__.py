{
    'name': 'Revoke Leave Request',
    'version': '17.0.0.1',
    'category': 'Time Off',
    'sequence': -100,
    'summary': 'Leave Revoke Request',
    'description': """Leave Revoke Request""",
    'author': 'Loyal IT Solution',
    'website': 'https://www.loyalitsolutions.com',
    'depends': ['base', 'mail', 'hr_holidays', 'hr', 'mrp','infinous_user_groups'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/revoke_leave_request_wizard_view.xml',
        'views/hr_leave_inherit_view.xml',

    ],
    'installable': True,
    'auto_install': False,
}
