from odoo import models, fields, api, _
from pytz import timezone



class EmployeeAttendanceRequestWizard(models.TransientModel):
    _name = 'employee.attendance.correction.wizard'
    _description = "Attendance Correction Request"
    _inherit = 'mail.thread'
    _rec_name='user_id'


    send_to = fields.Char(string="Send to", compute="_compute_mail")
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    correction_reason = fields.Html(string="Subject")
    send_to_emp = fields.Many2one('hr.employee', string='Send to Employee', default=lambda self: self._default_send_to_emp())

    def action_send_mail(self):
        active_id = self.env.context.get('active_id')

        if active_id:
            attendance_record = self.env['hr.attendance'].sudo().browse(active_id)
            user_tz = self.env.user.tz or 'UTC'

            user_timezone = timezone(user_tz)
            checkin = attendance_record.check_in.astimezone(user_timezone).strftime("%d %B")

            # check_out = attendance_record.check_out.astimezone(user_timezone).strftime("%d %B")


            mail_values = {
                'subject': f'Attendance Correction Request From {self.user_id.name} for {checkin}',
                'body_html': self.correction_reason,
                'email_to': self.send_to,
            }
            self.env['mail.mail'].sudo().create(mail_values).send()

            users = self.env['res.users'].browse(self.send_to_emp.user_id.id)

            notification_ids = []
            for purchase in users:
                notification_ids.append((0, 0, {
                    'res_partner_id': purchase.partner_id.id,
                    'notification_type': 'inbox'}))
            message = self.message_post(body=self.correction_reason,subject=f'Attendance Correction Request  From {self.user_id.name} for {checkin}',
                                        message_type='comment', subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)

            if message:
                message.write({'notification_ids': notification_ids})


    @api.model
    def _default_send_to_emp(self):
        current_user = self.env.user
        if current_user.employee_id and current_user.employee_id.parent_id:
            return current_user.employee_id.parent_id.id
        return False

    @api.model
    def default_get(self, fields):
        res = super(EmployeeAttendanceRequestWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')

        if active_id:
            attendance_record = self.env['hr.attendance'].sudo().browse(active_id)
            user_tz = self.env.user.tz or 'UTC'
            user_timezone = timezone(user_tz)
            checkin = attendance_record.check_in.astimezone(user_timezone).strftime("%d %B")
            res['correction_reason'] = f"Kindly approve my attendance correction request for {checkin}"
        return res

    @api.depends('user_id')
    def _compute_mail(self):
        current_user = self.env.user
        if current_user.employee_id and current_user.employee_id.parent_id:
            parent_email = current_user.employee_id.parent_id.work_email
            self.send_to = parent_email
        else:
            self.send_to = ""






