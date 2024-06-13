from odoo import models, fields, api, _


class EmployeeAttendanceRequest(models.Model):
    _name = 'employee.attendance.request'




    send_to = fields.Many2one('hr.employee', string="Send To", required=True, readonly= True)

    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    mail_to = fields.Selection([
        ('work', 'Work'),
    ], string='Email', help="""Email used to send the Request For Attendance.
                        - Work takes the email defined in "work email"
                        - Private takes the email defined in Private Information
                        - If the selected email is not defined, the available one will be used.""", default='work')

    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        current_user = self.env.user
        hr_managers = self.env['hr.employee'].sudo().search([('id','=',current_user.employee_id.parent_id.id)],limit=1)
        res['send_to'] = hr_managers.id
        return res
    
   

    
    

    mail_displayed = fields.Char(compute='_compute_mail_displayed')
    subject = fields.Char(string="Subject", required=True, default='Request For Attendance')
    message = fields.Html("Message")
    attachment_ids = fields.Many2many('ir.attachment')


    def validate_attendance_request(self):

        attachment_ids = [attachment.id for attachment in self.attachment_ids]
        att = self.env['ir.attachment'].browse(attachment_ids)
        att.write({'public': True})

        mail_user = self.send_to.user_id.id


        user = self.env['res.users'].browse(mail_user)


        post = self.env.user.partner_id.message_post(body=self.message, message_type='notification',
                                                         # subtype_xmlid='mail.mt_comment',
                                                         author_id=self.env.user.partner_id.id)
        if post:
                notification_ids = [(0, 0, {'res_partner_id': user.partner_id.id, 'mail_message_id': post.id}) for user
                                    in user]
                post.write({'notification_ids': notification_ids})

        mail_values = {
            'author_id': self.env.user.partner_id.id,
            'body_html': self.message,
            'email_from': self.env.user.email_formatted,
            'subject': self.subject,
            'attachment_ids': [(6, 0, attachment_ids)],

        }

        if self.mail_to == 'work' and self.send_to.work_email:
            mail_values['email_to'] = self.send_to.work_email

        mail = self.env['mail.mail'].create(mail_values)
        mail.send()

    @api.depends('send_to')
    def _compute_mail_displayed(self):
        for wizard in self:
            if wizard.send_to:
                wizard.mail_displayed = wizard.send_to.work_email
                
            else:
                wizard.mail_displayed = False
    
            
