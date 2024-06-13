# -*- coding: utf-8 -*-
{
    'name': "Infi Recruitment Request",

    'summary': "Infi Recruitment Request",

    'description': """
        Employee Recruitment Request
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Human Resources/Employees',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'mail', 'base', 'hr_payroll','infinous_user_groups'],
    # always loaded
    'data': ['security/ir.model.access.csv',
             'wizard/employee_recruitment_request_view.xml',
             'wizard/sending_offer_letter_view.xml',
             'views/infi_recruitment_request.xml',
             ],
    "license": "LGPL-3",
}
