# -*- coding: utf-8 -*-
{
    'name': "CRM Document BM Verification",

    'summary': """
        CRM student document BM verification""",

    'description': """
        CRM student document BM verification
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'asbm_application_form_website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/bm_security.xml',
        'wizard/bm_verification_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
