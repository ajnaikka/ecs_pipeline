from odoo import models, fields,api,_


class HrEmployeeAnnouncement(models.Model):
    _name = 'hr.employee.announcement'
    _description = 'Employee Announcements'

    subject = fields.Text(string="Subject")
    date = fields.Date(string="Date")
    user_id = fields.Many2one('res.users', 'User')
    company_id = fields.Many2one('res.company', string="Company")


