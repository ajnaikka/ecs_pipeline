
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Activity Enterprise',
    'version': '16.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Activities',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_activity',
        'openeducat_core_enterprise',
        'openeducat_student_progress_enterprise',
    ],
    'data': [

        'security/op_security.xml',
        'security/ir.model.access.csv',
        'wizards/progression_activity_wizard_view.xml',
        'views/openeducat_activity_portal.xml',
        'views/openeducat_activity_view.xml',
        'views/openeducat_progression_activity.xml',
        'views/student_progression_activity_portal.xml',
        'views/activity_type_view.xml',
        'reports/migration_report_view.xml',
        'reports/activity_progression_report.xml',
        'menus/activity_menu.xml'
    ],
    'demo': ['demo/progression_activity_demo.xml'],
    'images': [
        'static/description/openeducat_activity_enterprise_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 50,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
