# -*- coding: utf-8 -*-
{
    'name': "ASBM Corporate",

    'summary': """
        This module is used to create and assign corporate section in asbm project""",

    'description': """
        This module is used to create and assign corporate section in asbm project
    """,

    'author': "Loyal It Solutions",
    'website': "https://www.loyalitsolutions.com",

    'category': 'E-Learning',
    'version': '16.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core',
                'openeducat_assignment', 'openeducat_lesson', 'openeducat_fees',
                'openeducat_lesson', 'openeducat_activity'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/corporate_view.xml',
        'views/course_view.xml',
        'views/student_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
