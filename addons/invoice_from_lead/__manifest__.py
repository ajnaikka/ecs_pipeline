# -*- coding: utf-8 -*-
{
    'name': "invoice_from_lead",

    'summary': """
        """,

    'description': """
        This module is create invoice from crm lead.For that add is_product option in course creation.
        If it is product  course is created as product. When we create invoice course is add in invoice line.
    """,

    'author': "LOYAL IT SOLUTIONS",
    'website': "https://www.loyalitsolutions.com/",

    'category': 'CRM',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','openeducat_custom'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/crm_lead.xml',
        'views/account_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
