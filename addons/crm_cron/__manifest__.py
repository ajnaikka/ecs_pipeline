# -*- coding: utf-8 -*-
{
    'name': "crm cron",

    'summary': """ Run scheduled action that are automatically filtering and assigning leads 
        """,

    'description': """
         This module is automatically fetch all new leads and check repeated & fresh leads based on email and phone number. 
         Fresh leads are converted to opportunity and set to new stage.
         This fresh leads are assigning to sales person who comes in sales team based on specific rule.
         All duplicate leads are also assigning to their user and  send a notification to them .
    """,

    'author': "LOYAL IT SOLUTIONS",
    'website': "https://www.loyalitsolutions.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'crm',
    'version': '16.0.2',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','web', 'bus','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/cron.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],


}
