from odoo import models, fields, api, _
from lxml import etree


class EmployeeRevokeLeaveRequestWizard(models.TransientModel):
    _name = 'request.revoke.leave.wizard'
    _inherit = ['mail.thread']
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)

    start_date = fields.Date(default=lambda self: self.env.context.get('active_id') and self.env[
        'hr.leave'].browse(self.env.context['active_id']).request_date_from, readonly=True)
    end_date = fields.Date('End Date', default=lambda self: self.env.context.get('active_id') and self.env[
        'hr.leave'].browse(self.env.context['active_id']).request_date_to, readonly=True)

    def _default_send_to(self):
        user_employee_id = self.env.user.employee_id
        parent_id = user_employee_id.parent_id.id
        send_to_record = self.env['hr.employee'].search([('id', '=', parent_id)], limit=1)
        return send_to_record.id if send_to_record else False

    send_to_revoke = fields.Many2one('hr.employee', string="Send To", required=True, default=_default_send_to, readonly=True)



    mail_displayed = fields.Char(compute='_compute_mails_displayed')

    subject = fields.Char(string="Subject", required=True)

    def default_get(self, fields_list):
        defaults = super(EmployeeRevokeLeaveRequestWizard, self).default_get(fields_list)

        active_leave = self.env['hr.leave'].browse(self.env.context.get('active_id'))
        date_start = active_leave.request_date_from.strftime('%d-%m-%Y') if active_leave else ''
        date_to = active_leave.request_date_to.strftime('%d-%m-%Y') if active_leave else ''

        defaults['subject'] = f"Request For Revoking Leave From {date_start} to {date_to}"

        return defaults

    message = fields.Html("Message")
    attachment_ids = fields.Many2many('ir.attachment')

    def validate_request_revoke(self):

        if self.send_to_revoke.user_id.partner_id:
            attachment_ids = [attachment.id for attachment in self.attachment_ids]

            att = self.env['ir.attachment'].browse(attachment_ids)
            att.write({'public': True})

            mail_user = self.send_to_revoke.user_id.id

            user_revoke = self.env['res.users'].browse(mail_user)

            post = self.env.user.partner_id.message_post(body=self.message, message_type='notification',
                                                         subtype_xmlid='mail.mt_comment',
                                                         author_id=self.env.user.partner_id.id)

            if post:
                notification_ids = [(0, 0, {'res_partner_id': user.partner_id.id, 'mail_message_id': post.id}) for user
                                    in
                                    user_revoke]
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

    @api.depends('send_to_revoke')
    def _compute_mails_displayed(self):
        for wizard in self:
            if wizard.send_to_revoke:
                wizard.mail_displayed = wizard.send_to_revoke.work_email

            else:
                wizard.mail_displayed = False
