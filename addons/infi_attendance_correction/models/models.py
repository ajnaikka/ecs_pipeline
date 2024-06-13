# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

from datetime import datetime
from dateutil.relativedelta import relativedelta



class ResCompany(models.Model):
    _inherit = 'res.company'

    allow_attendance_correction = fields.Boolean(string="Allow Attendance Correction to employee",default=False)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def get_hr_user_work_email(self):
        """Fetch the work email of the HR user from the specified group."""
        hr_group = self.env.ref('infinous_user_groups.assigment_hr')
        hr_user = self.env['res.users'].sudo().search([('groups_id', 'in', hr_group.id)], limit=1)
        return hr_user and hr_user.work_email or False

    def employee_attendance_reminder(self):
        """Sending attendance reminder to employees on the last day of each month."""
        current_date = fields.Date.today()
        last_day_of_month = (current_date + relativedelta(day=31)).replace(day=current_date.day)

        employees = self.search([('work_email', '!=', False)])

        outgoing_mail = self.env['ir.mail_server'].sudo().search([], order='sequence', limit=1)
        hr_user_work_email = self.get_hr_user_work_email()

        for employee in employees:
            mail_content = "Hello " + employee.name + (",<br>Please ensure to submit your attendance for the current month."
                                                       "Also make corrections if any correction required.")

            main_content = {
                'subject': _('Attendance Reminder'),
                'author_id': self.env.user.partner_id.id,
                'body_html': mail_content,
                'email_to': employee.work_email,
                'email_from': hr_user_work_email or outgoing_mail.smtp_user,
            }

            self.env['mail.mail'].sudo().create(main_content).send()

    def smart_attendance_correction_request(self):
        self.ensure_one()
        all_child = self.with_context(active_test=False).search([('id', 'in', self.ids)])

        action = self.env["ir.actions.act_window"]._for_xml_id("infi_attendance_correction.attendance_correction_request_action")
        action['domain'] = [
            ('employee_id', 'in', all_child.ids)
        ]
        action['context'] = {'search_default_employee_id': self.id}
        return action

    def action_attendance_correction_request(self):
        company = self.env.user.company_id

        if company.allow_attendance_correction == True:
            request_record = self.env['attendance.correction'].create({
                'employee_id': self.id,
            })

            view_id = self.env.ref('infi_attendance_correction.attendance_correction_request_form').id

            return {
                'type': 'ir.actions.act_window',
                'name': 'Attendance Correction Request Form',
                'view_mode': 'form',
                'view_id': view_id,
                'res_model': 'attendance.correction',
                'target': 'current',
                'res_id': request_record.id,
                'context': {
                    'default_employee_id': self.id,
                }
            }
        else:
            # If the boolean is not true, you can return a message or perform another action
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Access Denied'),
                    'type': 'warning',
                    'message': _('Attendance correction requests are not allowed.'),
                }
            }



class AttendanceCorrection(models.Model):
    _name = 'attendance.correction'
    _description = 'Attendance Correction'
    _order = 'id desc'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    request_date = fields.Date(string='Request Date', format='%d-%m-%y')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('raise_correction_req', 'Attendance Correction Request to Manager'),
        ('issue_address', 'Issue Addressed'),
        ('corrected', 'Accepted & Corrected'),
        ('cancel', 'Rejected'),
        ('closed', 'Closed'),
    ], default='draft')


    comment = fields.Text(string="Comment")
    # email_to = fields.Many2one('res.partner', string="To", required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False,
                                 default=lambda self: self.env.company)

    def attendance_correction_request_button(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_attendance_correction.employee_attendance_correction_request_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'attendance.correction',
            'default_res_ids': [self.id],
            # 'default_partner_ids': [self.email_to.id],
            'default_raise_req_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': None,
            'force_email': True,
            'default_email_from': self.env.user.partner_id.email,
            'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        }

        if ctx:
            context.update(ctx)

        self.write({'state': 'raise_correction_req'})

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'views_id': compose_form_id,
            'target': 'new',
            'context': context,
        }

    def action_attendance_issue_address(self):
        for record in self:
            if record.state == 'raise_correction_req':
                record.write({'state': 'issue_address'})
        return True

    def action_attendance_accepted_corrected(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_attendance_correction.employee_attendance_accepted_corrected_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'attendance.correction',
            'default_res_ids': [self.id],
            # 'default_partner_ids': [self.email_to.id],
            'default_raise_req_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': None,
            'force_email': True,
            'default_email_from': self.employee_id.parent_id.work_email,
            'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        }

        if ctx:
            context.update(ctx)
        print(context, 'context')

        self.write({'state': 'corrected'})

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'views_id': compose_form_id,
            'target': 'new',
            'context': context,
        }
    def action_attendance_cor_rejected(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_attendance_correction.employee_att_cor_rejected_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'attendance.correction',
            'default_res_ids': [self.id],
            # 'default_partner_ids': [self.email_to.id],
            'default_raise_req_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': None,
            'force_email': True,
            'default_email_from': self.employee_id.parent_id.work_email,
            'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        }

        if ctx:
            context.update(ctx)
        print(context, 'context')

        self.write({'state': 'cancel'})

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'views_id': compose_form_id,
            'target': 'new',
            'context': context,
        }

    def close_att_button(self):
        for record in self:
            if record.state == 'corrected':
                record.write({'state': 'closed'})
        return True