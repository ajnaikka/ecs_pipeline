# -*- coding: utf-8 -*-
{
    'name': "Portal Policy",

    'summary': "Policy agree option in portal",

    'description': """ This module can be used to Policy agree option in portal.    """,

    'author': "Loyal IT Solutions PVT LTD",
    'website': "https://loyalitsolutions.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Portal',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal', 'hr'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        'views/employee_policy_views.xml',
        'views/employee_views.xml',
        'views/policy_history_views.xml',
        'views/portal_template_inherit.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
    'assets': {
        'web.assets_frontend': [
            'infi_portal_policy/static/src/js/policy_modal.js',
        ],
    },
}
