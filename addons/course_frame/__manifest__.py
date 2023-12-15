# -*- coding: utf-8 -*-
{
    'name': "Loyal Course Frame",

    'summary': """
        Customization added in course frame
        """,

    'description': """
        Customization added in course frame
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_custom','openeducat_core', 'asbm_main',  'website_slides'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/ir_sequence_data.xml',
        'wizards/course_frame_wizard_view.xml',
        'views/course_frame_views.xml',
        'views/media_request_view.xml',
        'views/content_development_view.xml',
        'views/masters_views.xml',
        'views/res_company_view.xml',
        'views/flip_book_view.xml',
        'views/views.xml',
        'views/subject_view.xml',

    ],
}
