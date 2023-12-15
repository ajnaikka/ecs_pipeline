# -*- coding: utf-8 -*-
{
    'name': "ASBM Application using Website",

    'summary': """
        """,

    'description': """

    """,

    'author': "Loyal",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '14.0.1',
     'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'openeducat_custom', 'website_crm', 'web', 'portal', 'lead_opportunity_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/signature_templates.xml',
        'views/student_employee_form.xml',
        'views/crm_lead.xml'
    ],
    'assets': {
        'website.assets_frontend': [
            '/asbm_application_form_website/static/src/css/style.css',
        ],

    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
