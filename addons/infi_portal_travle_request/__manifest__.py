# -*- coding: utf-8 -*-
{
    'name': "Travel Request For Portal User",

    'summary': "Travel Request For Portal User",

    'description': """
        Travel Request For Portal User
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Uncategorized',
    'version': '17.0.0.1',

    'depends': ['portal', 'inf_employee_portal','web'],
    'data': [

        "views/travel_request.xml",


    ],
    'assets': {
        'web.assets_frontend': [
            # '/infi_portal_travle_request/static/src/js/travel_request.js',

        ],

    },
    "license": "LGPL-3",
}

