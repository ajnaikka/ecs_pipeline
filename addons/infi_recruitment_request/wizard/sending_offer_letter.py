from odoo import models, fields, api


class EmployeeRecruitmentWizard(models.TransientModel):
    _name = 'sending.approval.wizard'
    _inherit = ['mail.thread']
    _rec_name = 'user_id'

    send_to = fields.Many2many('hr.employee', string="CC")
    user_id = fields.Many2one('res.users', 'Users', default=lambda self: self.env.user)
    hr_managers = fields.Many2many('hr.employee', string="HR Managers", compute='_compute_hr_managers')
    mail_to = fields.Selection([
        ('work', 'Work'),
    ], string='Email', help="""Email used to send the Sending Offer Letter.
                        - Work takes the email defined in "work email"
                        - Private takes the email defined in Private Information
                        - If the selected email is not defined, the available one will be used.""", default='work')

    subject = fields.Char(string="Subject", required=True, default='Sending Offer Letter')
    message = fields.Html("Message")
    attachment_ids = fields.Many2many('ir.attachment')
    email = fields.Char(string='Candidate Email')

    def to_cc(self):
        for wizard in self:
            attachment_ids = [attachment.id for attachment in wizard.attachment_ids]

            att = wizard.env['ir.attachment'].browse(attachment_ids)
            att.write({'public': True})

            email_to_list = [employee.work_email for employee in wizard.send_to]

            mail_values = {
                'author_id': wizard.env.user.partner_id.id,
                'auto_delete': True,
                'body_html': wizard.message,
                'email_from': wizard.env.user.email_formatted,
                'email_to': ', '.join(email_to_list),
                'subject': wizard.subject,
                'attachment_ids': [(6, 0, attachment_ids)],
            }

            mail = wizard.env['mail.mail'].sudo().create(mail_values)
            mail.send()

    def button_send_offer_letter(self):
        self.to_cc()
        for wizard in self:
            attachment_ids = [attachment.id for attachment in wizard.attachment_ids]

            att = wizard.env['ir.attachment'].browse(attachment_ids)
            att.write({'public': True})

            email_address = wizard.email

            mail_values = {
                'author_id': wizard.env.user.partner_id.id,
                'auto_delete': True,
                'body_html': wizard.message,
                'email_from': wizard.env.user.email_formatted,
                'email_to': email_address,
                'subject': wizard.subject,
                'attachment_ids': [(6, 0, attachment_ids)],
            }

            mail = wizard.env['mail.mail'].sudo().create(mail_values)
            mail.send()

    @api.depends('send_to', 'mail_to')
    def _compute_mail_displayed(self):
        for wizard in self:
            if wizard.send_to:
                wizard.mail_displayed = wizard.send_to[0].private_email if wizard.mail_to == 'private' else \
                    wizard.send_to[0].work_email
            else:
                wizard.mail_displayed = False
