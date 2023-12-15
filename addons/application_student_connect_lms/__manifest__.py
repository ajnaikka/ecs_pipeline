# -*- coding: utf-8 -*-
{
    'name': "Application - Student Connect LMS",

    'summary': """
        Connect student to LMS from admission application""",

    'description': """
        Connect student to LMS from admission application
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '16.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_admission', 'course_frame', 'website_slides'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/connect_lms_view.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
}
