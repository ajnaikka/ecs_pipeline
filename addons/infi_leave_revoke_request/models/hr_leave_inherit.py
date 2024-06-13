from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class EmployeeRevokeLeaveRequest(models.Model):
    _inherit = 'hr.leave'

    reason = fields.Char(string='Refusing Reason')

    def _validate_leave_request(self):
        """ Validate time off requests (holiday_type='employee')
        by creating a calendar event and a resource time off. """
        holidays = self.filtered(lambda request: request.holiday_type == 'employee' and request.employee_id)
        holidays._create_resource_leave()
        meeting_holidays = holidays.filtered(lambda l: l.holiday_status_id.create_calendar_meeting)
        meetings = self.env['calendar.event']
        if meeting_holidays:
            meeting_values_for_user_id = meeting_holidays._prepare_holidays_meeting_values()
            Meeting = self.env['calendar.event']
            for user_id, meeting_values in meeting_values_for_user_id.items():
                meetings += Meeting.with_user(user_id or self.env.uid).with_context(
                                allowed_company_ids=[],
                                no_mail_to_attendees=True,
                                calendar_no_videocall=True,
                                active_model=self._name
                            ).sudo().create(meeting_values)
        Holiday = self.env['hr.leave']
        for meeting in meetings:
            Holiday.browse(meeting.res_id).meeting_id = meeting


    @api.constrains('number_of_days_display', 'supported_attachment_ids', 'holiday_status_id.is_sick')
    def _check_attachments_required(self):
        for record in self:
            if record.number_of_days_display >= 3 and record.holiday_status_id.is_sick and not record.supported_attachment_ids:
                raise ValidationError("Attachments are required for leave requests with 3 or more leaves.")

    # def action_revoke_leave(self):
    #     for leave_request in self:
    #         employees = leave_request.employee_ids
    #         if employees:
    #             for employee in employees:
    #                 subject = 'Leave Request Revoked'
    #                 date_from = leave_request.request_date_from.strftime('%d-%m-%Y')
    #                 date_to = leave_request.request_date_to.strftime('%d-%m-%Y')
    #                 body = f" leave request of {employee.name} from {date_from} to {date_to} has been revoked."
    #
    #
    #                 mail_values = {
    #                     'subject': subject,
    #                     'body_html': body,
    #                     'email_to': employee.work_email,
    #                 }
    #
    #                 self.env['mail.mail'].create(mail_values).send()
    #                 employee.message_post(subject=subject, body=body, message_type='comment')
    #                 leave_request.message_post(subject=subject, body=body, message_type='comment')




    def action_draft(self):
        if any(holiday.state not in ['confirm', 'refuse','validate'] for holiday in self):
            raise UserError(_('Time off request state must be "Refused" or "To Approve" in order to be reset to draft.'))
        self.write({
            'state': 'draft',
            'first_approver_id': False,
            'second_approver_id': False,
        })
        if self.env.user.has_group('infinous_user_groups.reporting_manager'):
            for leave_request in self:
                employees = leave_request.employee_ids
                if employees:
                    for employee in employees:
                        subject = 'Leave Request Revoked'
                        date_from = leave_request.request_date_from.strftime('%d-%m-%Y')
                        date_to = leave_request.request_date_to.strftime('%d-%m-%Y')
                        body = f" leave request of {employee.name} from {date_from} to {date_to} has been revoked."


                        mail_values = {
                            'subject': subject,
                            'body_html': body,
                            'email_to': employee.work_email,
                        }

                        self.env['mail.mail'].sudo().create(mail_values).send()
                        employee.message_post(subject=subject, body=body, message_type='comment')
                        leave_request.message_post(subject=subject, body=body, message_type='comment')
        linked_requests = self.mapped('linked_request_ids')
        if linked_requests:
            linked_requests.action_draft()
            linked_requests.unlink()
        self.activity_update()
        return True


    def action_refusing_dup(self):

        if self.state in ['confirm', 'validate1', 'validate']:
            return {
                'name': _('Refuse Leave Request'),
                'type': 'ir.actions.act_window',
                'views': [(False, 'form')],
                'view_mode': 'form',
                'view_id': self.env.ref('infi_leave_revoke_request.employee_refused_leave_request_tree_view').id,
                'res_model': 'refuse.leave.request',
                'context': {'default_leave_id': self.id, 'default_from_date': self.request_date_from, 'default_to_date': self.request_date_to, 'default_employee_name_id': self.employee_id.id},
                # 'res_id': wizard.id,
                'target': 'new',
            }





    def action_refuse(self):

        current_employee = self.env.user.employee_id
        if any(holiday.state not in ['draft', 'confirm', 'validate', 'validate1'] for holiday in self):
            raise UserError(_('Time off request must be confirmed or validated in order to refuse it.'))

        self._notify_manager()
        validated_holidays = self.filtered(lambda hol: hol.state == 'validate1')
        validated_holidays.write({'state': 'refuse', 'first_approver_id': current_employee.id})
        (self - validated_holidays).write({'state': 'refuse', 'second_approver_id': current_employee.id})
        # Delete the meeting
        self.mapped('meeting_id').write({'active': False})
        # If a category that created several holidays, cancel all related
        linked_requests = self.mapped('linked_request_ids')
        if linked_requests:
            linked_requests.action_refuse()

        # Post a second message, more verbose than the tracking message
        for holiday in self:
            if holiday.employee_id.user_id:
                holiday.message_post(
                    body=_('Your %(leave_type)s planned on %(date)s has been refused',
                           leave_type=holiday.holiday_status_id.display_name, date=holiday.date_from),
                    partner_ids=holiday.employee_id.user_id.partner_id.ids)

        self.activity_update()
        template_values = {
            'name': 'Mail Regarding to Refuse Leave Request',
            'subject': self.reason,
            'body_html': """
                                               <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                                   <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                       <strong>Refuse Leave Request</strong>
                                                   </p>
                                                   <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                       <b>Dear %s,</b>
                                                   </p>
                                                   <br/>
                                                   <br/>
                                                   <p>
                                                       Leave Request has been cancelled,Please Contact Concerned assignment team for further enquiries
                                                   </p>
                                                   <br/>
                                                   <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                       Thank You
                                                   </p>
                                               </div>
                                           """ % (
                self.employee_id.name),
            'model_id': self.env.ref('hr_holidays.model_hr_leave').id,  # Corrected external ID reference
        }

        email_template = self.env['mail.template'].create(template_values)

        mail_template = self.env['mail.template'].browse(email_template.id)

        rendered_message = mail_template.body_html

        mail = self.env['mail.mail'].sudo().create({
            'subject': mail_template.subject,
            'body_html': rendered_message,
            'email_from': self.env.user.email_formatted,  # Use the actual sender email
            'email_to': self.employee_id.work_email,
        })

        mail.send()
        return True

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    is_sick = fields.Boolean(string='Sick')





class RefuseLeaveRequest(models.Model):
    _name = 'refuse.leave.request'

    reasons = fields.Char(string='Refusing Reason', required=True)
    leave_id = fields.Many2one('hr.leave', string="Leave", readonly=True)
    from_date = fields.Datetime('From Date')
    to_date = fields.Datetime('To Date')
    employee_name_id = fields.Many2one('hr.employee', 'Employee Name')

    @api.model_create_multi
    def create(self, vals_list):
        records = super(RefuseLeaveRequest, self).create(vals_list)
        for rec in records:
            rec.leave_id.sudo().write({
                "reason": rec.reasons
            })
            rec.leave_id.action_refuse()
        return records
