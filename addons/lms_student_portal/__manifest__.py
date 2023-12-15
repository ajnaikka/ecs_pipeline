# -*- coding: utf-8 -*-
{
    'name': "LMS Student Portal",

    'summary': """
        LMS in student portal""",

    'description': """
        LMS in student portal
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/eLearning',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_slides', 'openeducat_core_enterprise'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/lms_student_portal.xml',
        'data/lms_portal_menu.xml',
    ],
    'license': 'LGPL-3',
}
