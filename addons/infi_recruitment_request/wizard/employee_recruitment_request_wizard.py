from odoo import models, fields, api, _
from lxml import etree


class EmployeeRecruitmentWizard(models.TransientModel):
    _name = 'employee.recruitment.wizard'
    _inherit = ['mail.thread']
    _rec_name = 'user_id'

    send_to = fields.Many2one('hr.employee', string="Send To", required=True, domain="[('id','in',hr_managers)]")
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    hr_managers = fields.Many2many('hr.employee', string="HR Managers", compute='_compute_hr_managers')
    mail_to = fields.Selection([
        ('work', 'Work'),
    ], string='Email', help="""Email used to send the Request For Recruitment.
                        - Work takes the email defined in "work email"
                        - Private takes the email defined in Private Information
                        - If the selected email is not defined, the available one will be used.""", default='work')

    @api.depends('send_to')
    def _compute_hr_managers(self):
        for rec in self:
            hr_managers = self.env['hr.employee'].sudo().search(
                [('user_id.groups_id', 'in', [self.env.ref('hr.group_hr_manager').id])])
            rec.hr_managers = [(6, 0, hr_managers.ids)]

    mail_displayed = fields.Char(compute='_compute_mail_displayed')
    subject = fields.Char(string="Subject", required=True, default='Request For Recruitment ')
    message = fields.Html("Message")
    attachment_ids = fields.Many2many('ir.attachment')

    def validate_recruitment_request(self):
        if self.send_to.user_id.partner_id:
            attachment_ids = [attachment.id for attachment in self.attachment_ids]

            att = self.env['ir.attachment'].browse(attachment_ids)
            att.write({'public': True})

            mail_user = self.send_to.user_id.id

            user = self.env['res.users'].browse(mail_user)

            post = self.env.user.partner_id.message_post(body=self.message, message_type='notification',
                                                         subtype_xmlid='mail.mt_comment',
                                                         author_id=self.env.user.partner_id.id)

            if post:
                notification_ids = [(0, 0, {'res_partner_id': user.partner_id.id, 'mail_message_id': post.id}) for user
                                    in
                                    user]
                post.write({'notification_ids': notification_ids})

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

    @api.depends('send_to', 'mail_to')
    def _compute_mail_displayed(self):
        for wizard in self:
            if wizard.send_to:
                wizard.mail_displayed = wizard.send_to.private_email if self.mail_to == 'private' else wizard.send_to.work_email
            else:
                wizard.mail_displayed = False
