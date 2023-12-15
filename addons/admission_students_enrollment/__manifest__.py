# -*- coding: utf-8 -*-
{
    'name': "Admission - Students Enrollment",

    'summary': """
        Students enrollment in application and exam creation based on batch exam session""",

    'description': """
        Students enrollment in application and exam creation based on batch exam session
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_admission', 'crm_document_bdh_verification', 'course_frame', 'crm_admission_application', 'openeducat_exam','mail'],

    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
}
