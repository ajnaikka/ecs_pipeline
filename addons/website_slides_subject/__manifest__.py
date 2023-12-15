# -*- coding: utf-8 -*-
{
    'name': "Website Slides Subject",

    'summary': """
        Add subjects to your courses""",

    'description': """
        Add subjects to your courses
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/eLearning',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_slides', 'openeducat_core', 'website_slides_survey', 'course_frame'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_slides_subject/static/src/js/slides_course_fullscreen_player.js',
            'website_slides_subject/static/src/xml/website_slides_fullscreen.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
