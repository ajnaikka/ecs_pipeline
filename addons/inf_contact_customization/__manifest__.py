# -*- coding: utf-8 -*-
{
    'name': "Contact Customization",

    'summary': "Contact Customization",

    'description': """
        Contact Customization
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Contacts/Contacts',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts'],
    # always loaded
    'data': [
        "security/ir.model.access.csv",

        "views/contact.xml",


    ],
    "license": "LGPL-3",
}

