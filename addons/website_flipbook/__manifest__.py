# -*- coding: utf-8 -*-
{
    'name': "Website Flipbook",

    'summary': """
        Flipbook as website menu""",

    'description': """
        Flipbook as website menu
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/eLearning',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_slides', 'course_frame', 'website', 'openeducat_core'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/website_flipbook_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/website_data.xml',
    ],
    'license': 'AGPL-3',
}
