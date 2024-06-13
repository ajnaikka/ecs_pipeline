from odoo import models, fields, api, _


class EmployeePolicy(models.Model):
    _name = 'employee.policy'

    name = fields.Char('Policy Name')
    description = fields.Text('Policy')

    @api.model_create_multi
    def create(self, vals):
        policies = super(EmployeePolicy, self).create(vals)
        employees = self.env['hr.employee'].sudo().search([])
        if employees:
            for employee in employees:
                employee.have_agreed_policy = False
        return policies

    def write(self, vals):
        res = super(EmployeePolicy, self).write(vals)
        employees = self.env['hr.employee'].sudo().search([])
        if employees:
            for employee in employees:
                employee.have_agreed_policy = False
        return res


class EmployeePolicyHistory(models.Model):
    _name = 'employee.policy.history'

    date = fields.Datetime(string='Date', readonly=True)
    status = fields.Selection([('true', 'Agreed'), ('false', "Not Agreed")], string='Status', default='false',
                              readonly=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True)
    department = fields.Char('Department')
    employement_id = fields.Char('Employement Id')
    reporting_manager = fields.Char('Reporting Manager')

class Employee(models.Model):
    _inherit = 'hr.employee'

    have_agreed_policy = fields.Boolean('Have Agreed Policy', readonly=True)
