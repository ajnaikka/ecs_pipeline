from odoo import models, fields, api, _


class EmployeeProfile(models.Model):
    _name = 'employee.profile'

    name = fields.Char('Profile Name')
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)


    _sql_constraints = [
        ('name_uniq', 'unique(name)',
         'Hierarchy must be unique'),
    ]















