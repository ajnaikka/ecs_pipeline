# -*- coding: utf-8 -*-
{
    'name': "Employee Portal Customization",

    'summary': "Employee Portal Customization",

    'description': """
        Employee Portal Customization Setting
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Uncategorized',
    'version': '17.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['portal','employee_joining_letter','web', 'infi_portal_policy'],
    # always loaded
    'data': [
        # "security/ir.model.access.csv",
        # "views/employee_profile.xml",
        # "views/hr_expense.xml",
        "views/employee_portal.xml",
        "views/time_off_view.xml",
        "views/expense.xml",
        "views/employee_about_me.xml",


    ],
    'assets': {
            'web.assets_frontend': [
                'inf_employee_portal/static/src/js/portal_notification_pop_up.js',
            ],
        },

}