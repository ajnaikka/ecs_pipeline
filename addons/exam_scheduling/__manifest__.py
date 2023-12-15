# -*- coding: utf-8 -*-
{
    'name': "Exam Scheduling",

    'summary': """
        Exam scheduling""",

    'description': """
        Exam scheduling
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '16.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_exam', 'asbm_question_bucket'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/exam_add_survey.xml',
        'wizard/exam_invite_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
}
