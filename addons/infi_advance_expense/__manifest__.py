# -*- coding: utf-8 -*-
{
    'name': "Expense In Advance",

    'summary': "Expense In Advance",

    'description': """
        Expense In Advance
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Human Resources/Expenses',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','base','hr_expense','stock','stock_account','inf_hr_expense'],
    # always loaded
    'data': [
        "views/advance_expense.xml",

    ],
    "license": "LGPL-3",
}
