# -*- coding: utf-8 -*-
{
    'name': "CRM Admission Application",

    'summary': """
        Button in CRM to generate admission application in admission register and fee details in student""",

    'description': """
        Button in CRM to generate admission application in admission register and fee details in student
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'openeducat_admission', 'openeducat_custom', 'crm_document_bm_verification', 'openeducat_fees'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/crm_admission_application_views.xml',
        'views/lead_views.xml',
        'views/admission_views.xml',

    ],
    'license': 'LGPL-3',
}
