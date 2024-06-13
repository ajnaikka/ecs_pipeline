# -*- coding: utf-8 -*-
{
    'name': "Employee Certificate Request",

    'summary': "Employee Certificate Request",

    'description': """
        Employee Certificate Request
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Human Resources/Employees',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','hr_contract_sign','sign','web','mail','base','web_tour','hr_attendance','hr_payroll','infinous_user_groups','infi_raise_a_request'],
    # always loaded
    'data': [
        "security/ir.model.access.csv",
        'security/security.xml',
        "report/print_format_views.xml",

        'data/mail_template.xml',
        'data/cron.xml',
        "wizard/employee_certificate_request_wizard.xml",
        "wizard/employee_birthdate_date_filter_wizard.xml",
        "wizard/general_announcment_wizard.xml",

        "views/hr_employee.xml",
        "views/general_announcement.xml",
        "report/certificate_generation_pdf_template.xml",
        "views/employee_probation_details_view.xml",

    ],
    "license": "LGPL-3",

'assets': {
        'web.assets_backend': [
            'inf_employee_certificate_request/static/src/css/style.css',
        ],
    },
}

