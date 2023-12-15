# -*- coding: utf-8 -*-
{
    'name': "Exam Register",

    'summary': """
        Exam register""",

    'description': """
        Exam register
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'openeducat_core', 'openeducat_exam', 'admission_students_enrollment', 'exam_scheduling', 'exam_moderation'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/register_security.xml',
        'data/ir_sequence_data.xml',
        'views/student_course_view.xml',
        'views/views.xml',
    ],
    'license': 'LGPL-3',
}
