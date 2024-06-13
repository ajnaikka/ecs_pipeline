from odoo import models, fields, api



class ProductProduct(models.Model):
    _inherit = 'product.product'

    profile_id = fields.Many2one('employee.profile', string='Operational Level')
    expense_limit = fields.Float(string="Expense Limit")
