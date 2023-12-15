# -*- coding: utf-8 -*-
{
    'name': "ASBM Certificate",

    'summary': """
        This module is used to create Certificate section in asbm project""",

    'description': """
        This module is used to create certificate section in asbm project
    """,

    'author': "Loyal It Solutions",
    'website': "https://www.loyalitsolutions.com",

    'category': 'E-Learning',
    'version': '16.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core', 'asbm_batch_calendar', 'openeducat_exam', 'custom_background',
                'course_frame'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/certificate_view.xml',
        'views/certificate_template_view.xml',
        # 'views/ir_actions.xml',
        'reports/certificate_template.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
