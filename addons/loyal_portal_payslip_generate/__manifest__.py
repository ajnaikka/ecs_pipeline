# -*- coding: utf-8 -*-
{
    'name': "Portal Payslip",

    'summary': "Generate employee payslip from portal",

    'description': """ This module can be used to Generate employee payslip from portal.    """,

    'author': "Loyal IT Solutions PVT LTD",
    'website': "https://loyalitsolutions.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Portal',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal', 'hr', 'infinous_user_groups'],

    # always loaded
    'data': [
        'views/payslip_portal_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
    'assets': {
        'web.assets_frontend': [
        ],
    },
}
