# -*- coding: utf-8 -*-
{
    'name': "Openeducat Admission Custom",

    'summary': """
        Admission payment verification""",

    'description': """
        Admission payment verification
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_admission'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/admission_views.xml',
    ],
    'license': 'LGPL-3',
}
