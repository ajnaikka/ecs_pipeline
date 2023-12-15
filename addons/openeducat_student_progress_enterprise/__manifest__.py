
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Student Progress Enterprise',
    'version': '16.0.1.0',
    'category': 'Education',
    "sequence": 4,
    'summary': 'Manage Student progress',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_core_enterprise',

    ],
    'data': [
        'data/ir_sequence.xml',
        'data/student_progress_portal_menu.xml',
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'report/student_progression_report.xml',
        'report/report_menu.xml',
        'views/op_student_progress_portal.xml',
        'views/op_student_progress_data.xml',
        'views/assets.xml',
        'menu/progress_menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'openeducat_student_progress_enterprise/static/src/scss/student_progress.scss',
        ],
        'web.assets_tests': [
            'openeducat_student_progress_enterprise/static/tests/tours/student_progression_test.js',
        ],
    },
    'demo': ['demo/student_progression_demo.xml'],
    'images': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 50,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
