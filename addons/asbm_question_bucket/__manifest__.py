# -*- coding: utf-8 -*-
{
    'name': "ASBM Question Bucket",

    'summary': """
        This module is used to create question in asbm project""",

    'description': """
        This module is used to create question in asbm project
    """,

    'author': "Loyal It Solutions",
    'website': "https://www.loyalitsolutions.com",


    'category': 'E-Learning',
    'version': '16.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core', 'survey', 'openeducat_core_enterprise'],

    # always loaded
    'data': [
        'views/survey_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
