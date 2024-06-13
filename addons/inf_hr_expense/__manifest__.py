# -*- coding: utf-8 -*-
{
    'name': "Employee Expense Hierarchy Setting",

    'summary': "Employee Expense Hierarchy Setting",

    'description': """
        Employee Expense Hierarchy Setting
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Human Resources/Expenses',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','base','hr_expense','stock','stock_account','inf_employee_certificate_request'],
    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/employee_profile.xml",
        "views/hr_expense.xml",
        "views/hr_employee.xml",


    ],
    "license": "LGPL-3",
}

