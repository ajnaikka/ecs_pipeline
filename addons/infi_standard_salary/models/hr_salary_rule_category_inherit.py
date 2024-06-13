from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.salary.rule.category'

    standard_salary = fields.Selection([('basic_salary', 'Basic Salary'), ('house_allowance', 'House Allowance'),
                                       ('conveyence_allowance', 'Conveyence Allowance'),
                                       ('other_aalowance', 'Other Allowance'),
                                       ('special_allowance', 'Special Allowance')])
