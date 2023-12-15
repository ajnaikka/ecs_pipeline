# -*- coding: utf-8 -*-
{
    'name': "Exam Moderation",

    'summary': """
        If a student not able to qualify exam, moderation is possible with an approval""",

    'description': """
        If a student not able to qualify exam, moderation is possible with an approval
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '16.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'exam_scheduling'],

    # always loaded
    'data': [
        'security/moderation_security.xml',
        'security/ir.model.access.csv',
        'wizard/exam_moderation.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
}
