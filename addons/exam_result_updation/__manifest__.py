# -*- coding: utf-8 -*-
{
    'name': "Exam Result Updation",

    'summary': """
        Exam result updation""",

    'description': """
        Exam result updation
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_exam'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'license': 'LGPL-3',
}
