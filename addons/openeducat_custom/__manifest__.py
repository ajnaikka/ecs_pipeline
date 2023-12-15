# -*- coding: utf-8 -*-
{
    'name': "openeducat_custom",

    'summary': """
        """,

    'description': """
       Manage Course Type, Specialization
    """,

    'author': "LOYAL IT SOLUTIONS",
    'website': "https://www.loyalitsolutions.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CRM',
     'version': '16.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'openeducat_core', 'mail', 'openeducat_admission'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/course_type_views.xml',
        'views/specialization_view.xml',
        'views/res_partner.xml',
        'views/crm_lead.xml',
        'views/student.xml',
        'views/Lead_portal.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
