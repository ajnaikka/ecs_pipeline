# -*- coding: utf-8 -*-

{
    'name': 'stock report',
    'version': '17.0.0.1',
    'category': 'stock',
    'sequence': -100,
    'summary': 'stock report',
    'description': """stock report""",
    'author': 'Loyal IT Solution',
    'website': 'https://www.loyalitsolutions.com',
    'depends': ['base','stock','hr','infi_news_shoot_request','infinous_user_groups'],
    'data': [

        # 'security/security.xml',
        'views/stock_report.xml'


    ],
    'installable': True,
    'auto_install': False,
}
