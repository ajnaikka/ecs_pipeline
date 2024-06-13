from odoo import models, fields, api, _


class Employee(models.Model):
    _inherit = 'hr.employee'

    profile_id = fields.Many2one('employee.profile', string='Operational Level')














