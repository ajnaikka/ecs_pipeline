
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

{
    'name': 'OpenEduCat Fees Enterprise',
    'version': '16.0.1.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Fees',
    'complexity': "easy",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    'depends': [
        'openeducat_fees',
        'openeducat_core_enterprise',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/before_fees_reminder_mail_template.xml',
        'data/after_fees_reminder_mail_template.xml',
        'data/server_action_view.xml',
        'views/fees_terms_view.xml',
        'views/service_cron.xml',
        'views/student_fees_details.xml',
        'wizard/student_invoice_wizard_view.xml',
        'menus/fees_detail_menu.xml',
    ],
    'demo': [
        'demo/fees_reminder_demo.xml',
    ],
    'images': [
        'static/description/openeducat_fees_enterprise_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 100,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://www.openeducat.org/plans'
}
