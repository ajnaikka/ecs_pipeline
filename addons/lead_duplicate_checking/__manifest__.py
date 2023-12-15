# -*- coding: utf-8 -*-
{
    'name': "Lead Duplicate Checking",

    'summary': """
        Lead duplicate checking and lead to opportunity conversion""",

    'description': """
        Lead duplicate checking and lead to opportunity conversion
    """,

    'author': "LOYAL IT SOLUTIONS",
    'website': "https://www.loyalitsolutions.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'crm',
    'version': '16.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/crm_duplicate_check_view.xml',
        'views/crm_stage_view.xml',
        'views/crm_lead_view.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'lead_duplicate_checking/static/src/views/*.js',
            # 'lead_duplicate_checking/static/src/views/*.xml',
            'lead_duplicate_checking/static/src/js/duplicate_checking.js',
            'lead_duplicate_checking/static/src/xml/duplicate_check.xml',
        ],
    },
}
