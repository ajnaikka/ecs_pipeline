from odoo import models, fields, api, exceptions, _
import base64
import pdfkit


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    type = fields.Selection([
        ('normal','Normal Expense'),
        ('advance','Advance Expense'),
    ],default="normal",string='Type Of Expense')


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    type = fields.Selection([
        ('normal','Normal Expense'),
        ('advance','Advance Expense'),
    ], compute='_compute_from_expense',string='Type Of Expense')

    @api.depends('expense_line_ids')
    def _compute_from_expense(self):
        for rec in self:
            print('okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            if rec.expense_line_ids:
                last_expense_line = rec.expense_line_ids[-1]
                rec.type = last_expense_line.type
            else:
                rec.type = False
