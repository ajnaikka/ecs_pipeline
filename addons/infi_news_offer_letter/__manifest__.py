# # -*- coding: utf-8 -*-
{
    'name': "Offer letter",

    'summary': "Offer letter",

    'description': """
        Offer Letter
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Sales/Sales',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts','sale','stock','sale_stock'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/offer_letter.xml',
        'reports/offer_letter_temp.xml',
        'views/offer.xml',

    ],
    "license": "LGPL-3",
}