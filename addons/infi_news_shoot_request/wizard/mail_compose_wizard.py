from odoo import models, fields, api

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    shoot_req_id = fields.Many2one('shoot.request')
    # req_id_bool = fields.Boolean('Partner Hide')

    def action_send_mail(self):
        result = super(MailComposeMessage, self).action_send_mail()
        emp_shoot = self.shoot_req_id
        print(emp_shoot,'shoot')

        if emp_shoot:
            ter_record = emp_shoot

            if ter_record.state == 'draft':
                ter_record.write({'state': 'shoot_req'})
                print(ter_record)

                ter_record_mang = ter_record.user_id.id

                department_users = self.env['res.users'].browse(ter_record_mang)

                post = self.env.user.partner_id.message_post(body=self.shoot_req_id.comment, message_type='notification',
                                                             subtype_xmlid='mail.mt_comment',
                                                             author_id=self.env.user.partner_id.id)
                print(post)
                notification_ids = []
                for user in department_users:
                    notification_ids.append((0, 0, {'res_partner_id': user.partner_id.id, 'mail_message_id': post.id}))

                self.env['mail.message'].create({
                    'message_type': "notification",
                    'body': "Shoot Request For Camera Form",
                    'subject': "Shoot Request For Camera Form",
                    'partner_ids': [(4, user.partner_id.id) for user in department_users],
                    'model': ter_record._name,
                    'res_id': ter_record.id,
                    'notification_ids': notification_ids,
                    'author_id': self.env.user.partner_id.id
                })
            

            elif ter_record.state == 'shoot_req' and ter_record.is_to_store_in_charge == True:
                ter_record.write({'state': 'to_storeperson'})

                ter_record_mang = ter_record.user_id.id

                department_users = self.env['res.users'].browse(ter_record_mang)

                post = self.env.user.partner_id.message_post(body=self.shoot_req_id.comment, message_type='notification',
                                                             subtype_xmlid='mail.mt_comment',
                                                             author_id=self.env.user.partner_id.id)

                notification_ids = []
                for user in department_users:
                    notification_ids.append((0, 0, {'res_partner_id': user.partner_id.id, 'mail_message_id': post.id}))

                self.env['mail.message'].create({
                    'message_type': "notification",
                    'body': "Confirmation regarding camera unit Assign",
                    'subject': "Shoot Request For Camera Form",
                    'partner_ids': [(4, user.partner_id.id) for user in department_users],
                    'model': ter_record._name,
                    'res_id': ter_record.id,
                    'notification_ids': notification_ids,
                    'author_id': self.env.user.partner_id.id
                })

        return result

