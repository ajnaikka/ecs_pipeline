# -*- coding: utf-8 -*-
{
    'name': "asbm_main",

    'summary': """
        All modules are added its depends""",

    'description': """
        All modules will install after completing this installation.
    """,

    'author': "LOYAL IT SOLUTIONS",
    'website': "https://www.loyalitsolutions.com/",
    'category': 'OpenEducat',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                # 'asbm_application_form_website',
                # 'base_accounting_kit',
                # 'bi_import_chart_of_accounts',
                # 'crm_cron',
                # 'openeducat_activity',
                # 'openeducat_admission',
                # 'openeducat_assignment',
                # 'openeducat_attendance',
                # 'openeducat_classroom',
                'openeducat_core',
                'openeducat_custom',
                # 'openeducat_erp',
                # 'openeducat_exam',
                # 'openeducat_facility',
                # 'openeducat_fees',
                # 'openeducat_library',
                # 'openeducat_parent',
                # 'openeducat_timetable',
                # 's2u_online_appointment',
                # 'voip',
                # 'voip_crm',
                # 'web_mobile',
                # 'web_openeducat',
                'project'
                ],
                # 'web_responsive'

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/project_view.xml',
        # 'views/course_view.xml',
        'views/subject_specialization.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
