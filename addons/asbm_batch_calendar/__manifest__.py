# -*- coding: utf-8 -*-
{
    'name': "ASBM Batch Calendar",

    'summary': """
        This module is used to manage the course exam and certification dates""",

    'description': """
        This module is used to manage the course exam and certification dates
    """,

    'author': "Loyal It Solutions",
    'website': "https://www.loyalitsolutions.com",

    'category': 'E-Learning',
    'version': '16.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core', 'course_frame'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/batch_view.xml',
        'views/batch_calendar_view.xml',
        'views/batch_month_view.xml',
        'views/exam_view.xml',
        'views/course_category_view.xml',
        'views/course_view.xml',
    ],
    # only loaded in demonstration mode

}
