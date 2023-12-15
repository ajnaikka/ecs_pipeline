# -*- coding: utf-8 -*-
{
    'name': "Flipbook Student Portal",

    'summary': """
        Flipbook in student portal""",

    'description': """
        Flipbook in student portal.
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/eLearning',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core_enterprise', 'openeducat_web', 'portal'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
        'data/flipbook_portal_menu.xml',
    ],
    'license': 'LGPL-3',
}
