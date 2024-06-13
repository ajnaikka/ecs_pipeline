from odoo import models, fields, api


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    compensatory_req_id = fields.Many2one('compensatory.request')
    comp_leave_bool = fields.Boolean('Compensatory')
    date_from = fields.Date(string='Comp off request against')
    date_to = fields.Date(string='Comp off requested for')

    def action_send_mail(self):
        result = super(MailComposeMessage, self).action_send_mail()
        comp_req = self.compensatory_req_id

        ter_record = self.env['compensatory.request'].browse(comp_req.id)

        if ter_record.state == 'draft' and self.comp_leave_bool:
            ter_record.state = 'to_reporter'
        elif ter_record.state == 'to_reporter' and not self.comp_leave_bool:
            ter_record.write({'state': 'to_hr'})
        ter_record_mang = self.env.user.id

        department_users = self.env['res.users'].browse(ter_record_mang)

        message_body = ""
        post = self.env.user.partner_id.message_post(
            body=message_body,
            subject="Compensatory Request Form",
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        print(post)
        notification_ids = []
        for user in department_users:
            notification_ids.append((0, 0, {'res_partner_id': user.partner_id.id, 'mail_message_id': post.id}))

        self.env['mail.message'].create({
            'message_type': "notification",
            'body': message_body,
            'subject': "Compensatory Request Form",
            'partner_ids': [(4, user.partner_id.id) for user in department_users],
            'model': ter_record._name,
            'res_id': ter_record.id,
            'notification_ids': notification_ids,
            'author_id': self.env.user.partner_id.id
        })

        return result
