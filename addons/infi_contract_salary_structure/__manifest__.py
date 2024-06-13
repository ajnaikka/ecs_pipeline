# -*- coding: utf-8 -*-
{
    'name': "Contract Salary Structure",

    'summary': "Contract Salary Structure",

    'description': """
        Contract Salary Structure
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Human Resources/Attendance',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','base','hr_expense','stock','hr_attendance','hr_contract','hr_payroll'],
    # always loaded
    'data': ['views/hr_contract_inherit_view.xml',
             'views/hr_payroll_structure_type_inherit_view.xml',
             'views/hr_contract_type_inherit_view.xml'],
    "license": "LGPL-3",
}

