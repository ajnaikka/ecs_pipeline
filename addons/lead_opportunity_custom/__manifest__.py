# -*- coding: utf-8 -*-
{
    'name': "Lead to Opportunity Customization",

    'summary': """
        Customization in lead to opportunity conversion""",

    'description': """
        Customization in lead to opportunity conversion
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'openeducat_custom'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/mail_template_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
