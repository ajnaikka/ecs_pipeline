# -*- coding: utf-8 -*-
{
    'name': "CRM Document BDH Verification",

    'summary': """
        CRM student document BDH verification""",

    'description': """
        CRM student document BDH verification
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'asbm_application_form_website', 'crm_admission_application', 'crm_document_bm_verification'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/bdh_security.xml',
        'wizard/line_bdh_verification_views.xml',
        'wizard/bdh_verification_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
