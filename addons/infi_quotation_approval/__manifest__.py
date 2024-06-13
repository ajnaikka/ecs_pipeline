# -*- coding: utf-8 -*-
{
    'name': "Submit for Quotation Approval",

    'summary': "Submit for Quotation Approval",

    'description': """ This module can be used to Submit for Quotation Approval.    """,

    'author': "Loyal IT Solutions PVT LTD",
    'website': "https://loyalitsolutions.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'hr','product','mail','hr_payroll','purchase_order_approval','infinous_user_groups'],


    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/quotation_approval.xml',
        'wizard/quotation_wizard.xml',
        'wizard/quotation_higher.xml',
    ],

}


