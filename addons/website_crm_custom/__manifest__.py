# -*- coding: utf-8 -*-
{
    'name': "Website CRM - Custom",

    'summary': """
        Enquiry button in Course Sidebar""",

    'description': """
        Enquiry button in Course Sidebar
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/Website',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_crm', 'website_slides', 'asbm_website_course_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
}
