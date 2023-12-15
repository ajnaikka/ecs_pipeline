
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'Openeducat Lesson Enterprise',
    'version': '16.0.1.0',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Manage Lesson Planning',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_timetable',
        'openeducat_parent'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/op_lesson_security.xml',
        'data/ir_sequence.xml',
        'views/lesson_view.xml',
        'menus/openeducat_lesson_menu.xml',
        'report/lesson_menu.xml',
        'report/report_lesson_planning.xml',
    ],
    'demo': [
        'demo/op_lesson_demo.xml'
    ],
    'images': [
        'static/description/openeducat_lesson_banner.jpg'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 50,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans',
}
