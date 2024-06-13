# -*- coding: utf-8 -*-

{
    'name': 'Image checkin',
    'version': '2.0',
    'category': 'Tool',
    'sequence': 6,
    'author': 'ErpMstar Solutions',
    'summary': "Allow you to capture image from your webcam in image widget.",
    'description': "Allow you to capture image from your webcam in image widget.",
    'depends': ['hr_attendance', 'web', 'hr', 'base','barcodes'],
    'data': [
        'views/my_attendance_menu.xml',
        # 'views/views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'infi_checkinout/static/src/components/attendance_menu/attendance_menu.js',
            'infi_checkinout/static/src/components/attendance_menu/attendance_menu.xml',
        ],

    },

    'application': True,
    'installable': True,
    'auto_install': False,
    'price': 10,
}
