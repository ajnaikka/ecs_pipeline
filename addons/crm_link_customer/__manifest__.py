# -*- coding: utf-8 -*-
{
    'name': "CRM - Link to Customer",

    'summary': """
        Link to customer and send invitation in opportunity""",

    'description': """
        Link to customer and send invitation in opportunity
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'lead_opportunity_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/link_customer_view.xml',
        'views/views.xml',
    ],
    'license': 'LGPL-3',
}
