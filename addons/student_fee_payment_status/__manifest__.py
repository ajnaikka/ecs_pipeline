# -*- coding: utf-8 -*-
{
    'name': "Student Fees Payment Status",

    'summary': """
        Payment status in student fees details""",

    'description': """
        Payment status in student fees details
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_fees', 'openeducat_fees_enterprise'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    'license': 'LGPL-3',
}
