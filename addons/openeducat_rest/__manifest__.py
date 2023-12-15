
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    OpenEduCat Inc.
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################


{
    "name": "OpenEduCat REST API",
    "summary": """Restful API for OpenEduCat""",
    "version": "16.0.1.0",
    "category": "Extra Tools",
    'author': 'OpenEduCat Inc',
    'website': 'http://www.openeducat.org',
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/rest_menu.xml",
        "views/rest_token_view.xml",
    ],
    "images": [
        'static/description/banner.png'
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "license": "Other proprietary",
    "price": 99.00,
    "currency": 'EUR',
}
