from odoo import models, fields, api, _
from datetime import datetime

class HrEmployeeCertificate(models.TransientModel):
    _name = 'hr.employee.certificate.request.wizard'
    _inherit = ['mail.thread']
    _rec_name = 'user_id'

    send_to = fields.Many2one('hr.employee', string="Send To", required=True,default=lambda self: self._get_default_hr_manager())
    employee_id = fields.Many2one('hr.employee',string="Employee")
    current_date = fields.Date(string="Date",default=datetime.now(),readonly=True)
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company)
    current_employee_user = fields.Many2one('hr.employee', string="Employee User",default=lambda self:self.env.user.employee_id.id)

    def _get_default_hr_manager(self):
        hr_employee = self.env.user.employee_id.hr_manager_id.id
        return hr_employee

    mail_to = fields.Selection([
        ('work', 'Work'),
        # ('private', 'Private'),
    ], string='Email', help="""Email used to send the Certificate request.
                    - Work takes the email defined in "work email"
                    - Private takes the email defined in Private Information
                    - If the selected email is not defined, the available one will be used.""", default='work')

    mail_displayed = fields.Char(compute='_compute_mail_displayed')
    subject = fields.Char(string="Subject", required=True, default='Certificate Request')
    prob_sub = fields.Char(string="Subject", required=True, default='Regarding Probationary Period ending')
    message = fields.Html("Message")
    attachment_ids = fields.Many2many('ir.attachment')
    certificate_bool = fields.Boolean('certificate')

    def validate_certificate_request(self):
        if self.send_to.user_id.partner_id:
            attachment_ids = self.attachment_ids.ids
            att_records = self.env['ir.attachment'].sudo().browse(attachment_ids)
            att_records.write({'public': True})

            mail_user = self.send_to.user_id.id
            users = self.env['res.users'].sudo().search([('id', '=', mail_user)])


            if self.employee_id and users:
                for user in users:
                    vals = {
                        'employee_id': self.employee_id.id,
                        'date': self.current_date,
                        'attachment_ids': [(6, 0, attachment_ids)],
                        'company_id': user.company_id.id,
                        'user_ids': [(4, user.id), (4, self.env.user.id)]
                    }

                    self.env['employee.probation.details'].sudo().create(vals)

            if users:
                notification_ids = [(0, 0, {
                    'res_partner_id': user.partner_id.id,
                    'notification_type': 'inbox'
                }) for user in users]


            self.env['mail.message'].sudo().create({
                'message_type': "notification",
                'email_from': self.mail_displayed,
                'body': self.message,
                'subject': self.subject,
                'partner_ids': [(4, user.partner_id.id) for user in users],
                'model': 'hr.employee',
                'res_id': self.current_employee_user.id,
                'notification_ids': notification_ids,
                'author_id': self.env.user.partner_id and self.env.user.partner_id.id,
                'attachment_ids': [(4, att.id) for att in att_records]
            })

            mail_values = {
                'author_id': self.env.user.partner_id.id,
                'auto_delete': True,
                'body_html': self.message,
                'email_from': self.env.user.email_formatted,
                'email_to': self.mail_displayed,
                'subject': self.subject,
                'attachment_ids': [(6, 0, attachment_ids)],
            }

            self.env['mail.mail'].sudo().create(mail_values).send()

            if self.certificate_bool:

                certificate_vals = {
                    'send_to': self.send_to.id,
                    'company_id': self.company_id.id,
                    'user_id': self.user_id.id,
                    'attachment_ids': [(6, 0, self.attachment_ids.ids)],
                    'date': fields.Date.today(),

                }
                self.env['employee.certificate.details'].sudo().create(certificate_vals)







    @api.depends('send_to', 'mail_to')
    def _compute_mail_displayed(self):
        for wizard in self:
            if wizard.send_to:
                wizard.mail_displayed = wizard.send_to.private_email if self.mail_to == 'private' else wizard.send_to.work_email
            else:
                wizard.mail_displayed = False
















