from odoo import models, fields, api, _
from datetime import datetime

class HrEmployeeGeneralAnnouncment(models.TransientModel):
    _name = 'hr.employee.general.announcement.wizard'
    _inherit = ['mail.thread']
    _rec_name = 'user_id'

    subject = fields.Text(string="Subject")
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company)

    def save_announcement(self):
        announcement = self.env['hr.employee.announcement'].create({
            'subject': self.subject,
            'date':fields.date.today(),
        })

        employees = self.env['hr.employee'].search([])

        for employee in employees:
            employee.message_post(body=f"New announcement: {announcement.subject}",
                                  message_type='comment', author_id=self.env.user.partner_id.id,
                                  )

        return {'type': 'ir.actions.act_window_close'}




















