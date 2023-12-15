# -*- coding: utf-8 -*-
{
    'name': "website_subsection_control",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website_slides'],

    # always loaded
     'data': [
        'views/slide_channel_views.xml',
        'views/slide_slide_views.xml',
        'views/website_slides_templates_course.xml',
        'views/survey_templates.xml',

    ],
    'demo': [
        'data/survey_demo.xml',
        'data/slide_slide_demo.xml',
        'data/survey.user_input.line.csv',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_subsection_control/static/src/scss/website_slides_survey.scss',
            'website_subsection_control/static/src/js/slides_upload.js',
            # 'website_subsection_control/static/src/js/slides_course_fullscreen_player.js',
            'website_subsection_control/static/src/xml/website_slide_upload.xml',
            'website_subsection_control/static/src/xml/website_slides_fullscreen.xml',
        ],
        'survey.survey_assets': [
            'website_subsection_control/static/src/scss/website_slides_survey_result.scss',
        ],
    },
    'license': 'LGPL-3',
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
