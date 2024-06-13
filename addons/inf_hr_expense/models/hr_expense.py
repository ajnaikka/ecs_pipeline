from odoo import models, fields,api
from odoo.exceptions import ValidationError

class Expense(models.Model):
    _inherit = 'hr.expense'

    profile_id = fields.Many2one('employee.profile', string='Operational Level', related='product_id.profile_id')
    emp_profile_id = fields.Many2one('employee.profile',string="Employee Hierarchy", related='employee_id.profile_id')
    expense_limit = fields.Float(string="Expense Limit",related='product_id.expense_limit',store=True)

    @api.onchange('total_amount_currency')
    def _onchange_total_amount_currency(self):
        for expense in self:
            if expense.total_amount_currency > expense.expense_limit:
                warning_msg = {
                    'title': 'Warning!',
                    'message': 'Entered total expense is above the expense limit.'
                }
                return {'warning': warning_msg}
























