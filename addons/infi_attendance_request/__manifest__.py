# -*- coding: utf-8 -*-
{
    'name': "Employee Attendance Request",

    'summary': "Employee Attendance Request",

    'description': """
        Employee Punch in operation forgot , sending request for attendance
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Human Resources/Attendance',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','base','hr_expense','stock','hr_attendance','mail'],
    # always loaded
    'data': ['security/ir.model.access.csv',
            'views/attendance_request_view.xml',
             'wizard/attendance_request_wizard.xml',
             'views/hr_attendance.xml',],
    "license": "LGPL-3",
}

