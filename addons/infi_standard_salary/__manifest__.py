{
    'name': "Standard Salary",

    'summary': "Employee Salary Structure",

    'description': """
    Employee Salary Structure 
   """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    'category': 'Human Resources/Employees',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'mail', 'base', 'hr_payroll', ],
    # always loaded
    'data': [
        'views/hr_employee_inherit_view.xml',
        'views/hr_salary_rule_category_inherit_view.xml',
        'views/hr_salary_rule_inheirt_view.xml',
    ],
    "license": "LGPL-3",
}
