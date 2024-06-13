{
    'name': "Budget Restriction",

    'summary': "Budget Restriction",

    'description': """Budget Restriction , if we planned a budget amount do not cross the amount in the expenses and purchses """,

    'author': "Loyal IT Solutions PVT LTD",
    'website': "https://loyalitsolutions.com/",

    'category': 'Budget',
    'version': '0.2',

    'depends': ['base', 'account','account_accountant', 'hr','purchase','account_budget'],

    'data': [
        'views/crossovered_budget_inherited_view.xml'
    ],
    'demo': [],
    'assets': { },
}
