import pytz

from collections import defaultdict
from datetime import datetime, timedelta
from operator import itemgetter
from pytz import timezone
from odoo.exceptions import MissingError, ValidationError

from odoo import models, fields, api, exceptions, _
from odoo.addons.resource.models.utils import Intervals
from odoo.tools import format_datetime
from odoo.osv.expression import AND, OR
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import AccessError
from odoo.tools import format_duration
from datetime import datetime


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'


    componsatory_hours = fields.Float(string='Compensatory Hours',compute='_compute_componsatory_hours')
    is_holiday = fields.Boolean(string='Is Holiday')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('taken', 'Taken'),
    ], default='draft')

    @api.depends('check_in')
    def _compute_display_name(self):
        for project in self:
            check_date = project.check_in.date()
            formatted_date = check_date.strftime('%d/%m/%y')
            if project.check_in:
                project.display_name = "[" + formatted_date + "]" if check_date else ""
            else:
                project.display_name = ""

    @api.model
    def create(self, vals):
        if 'employee_id' in vals and 'check_in' in vals:
            employee_id = vals['employee_id']
            check_in_date = fields.Datetime.from_string(vals['check_in']).date()

            # Check if employee_id is valid
            employee = self.env['hr.employee'].browse(employee_id)
            req = self.env['shift.request'].search(
                [('shift_from', '=', check_in_date), ('employee_id', '=', employee.id)])
            if not employee:
                # Handle case where employee is not found
                # You can log an error or raise an exception
                raise ValueError("Employee not found for ID: %s" % employee_id)

            # Check if employee has a contract
            if not employee.contract_id:
                raise ValueError("Employee %s does not have a contract" % employee.name)

            resource_calendar = employee.contract_id.resource_calendar_id
            if not resource_calendar:
                raise ValueError("No resource calendar found for employee %s" % employee.name)

            # Fetch public holidays that fall within the check-in date
            public_holidays = resource_calendar.global_leave_ids.filtered(
                lambda leave: leave.date_from.date() <= check_in_date <= leave.date_to.date())

            # Check if the login date is a public holiday or Sunday and the employee has compensatory hours
            if (public_holidays or check_in_date.weekday() == 6) or req.shifts_count_in_week > 5:
                vals.update({'is_holiday': True, 'status': 'approved'})

        return super(HrAttendance, self).create(vals)

    @api.depends('check_in','check_out')
    def _compute_componsatory_hours(self):
        for attendance in self:
            if attendance.check_out and attendance.check_in and attendance.employee_id and attendance.is_holiday:
                calendar = attendance._get_employee_calendar()
                resource = attendance.employee_id.resource_id
                tz = timezone(calendar.tz)
                check_in_tz = attendance.check_in.astimezone(tz)
                check_out_tz = attendance.check_out.astimezone(tz)
                lunch_intervals = calendar._attendance_intervals_batch(
                    check_in_tz, check_out_tz, resource, lunch=True)
                attendance_intervals = Intervals([(check_in_tz, check_out_tz, attendance)]) - lunch_intervals[resource.id]
                delta = sum((i[1] - i[0]).total_seconds() for i in attendance_intervals)
                attendance.componsatory_hours = delta / 3600.0
            else:
                attendance.componsatory_hours = False

    def action_status(self):
        self.status = 'taken'
class CompensatoryRequest(models.Model):
    _name = 'compensatory.request'
    _description = 'Compensatory Request'
    _order = 'id desc'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    issued_date = fields.Date(string='Issued Date', format='%d-%m-%y')
    request_date = fields.Date(string='Request Date', format='%d-%m-%y')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_reporter', 'Request To Reporting Manager'),
        ('to_hr', 'Request to hr'),
        ('cancel', 'Canceled'),
        ('approved', 'Approved'),
    ], default='draft')
    date_from = fields.Date(string='Comp off request against')
    date_to = fields.Date(string='Comp off request for')
    attendance_id = fields.Many2one('hr.attendance', string="Comp off request against",
                                    domain="[('employee_id', '=', employee_id), ('status', '=', 'approved')]")
    leave_count = fields.Integer(string='Number of Compensatory Leaves', compute='_compute_compensatory_leaves')

    @api.depends('employee_id')
    def _compute_compensatory_leaves(self):
        for record in self:
            if record.employee_id:
                Attendance = self.env['hr.attendance']
                print(Attendance,'attendance')
                count = Attendance.search_count([('employee_id', '=', record.employee_id.id),('status','=','approved')])
                print(count)
                record.leave_count = count
            else:
                record.leave_count = 0

    def compensatory_request_button(self,ctx=None):
        if self.leave_count <= 0:
            raise ValidationError("No sufficent Compensatory Benefit")
        else:
            self.state = 'to_reporter'
            self.request_date = fields.Date.today()
            template = self.env.ref('infi_compensatory_request.leave_request_email')
            compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

            context = {
                'default_model': 'compensatory.request',
                'default_res_ids': [self.id],
                'default_compensatory_req_id': self.id,
                'default_use_template': bool(template),
                'default_template_id': template.id,
                'default_composition_mode': 'comment',
                'default_attachment_ids': None,
                'force_email': True,
                'default_email_from': self.env.user.partner_id.email,
                'default_partner_id_bool': True,
                'default_comp_leave_bool': True,
                'default_partner_id': self.employee_id.parent_id.user_partner_id.id
            }

            if ctx:
                context.update(ctx)

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
    def req_hr(self,ctx=None):
        template = self.env.ref('infi_compensatory_request.leave_request_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'compensatory.request',
            'default_res_ids': [self.id],
            'default_compensatory_req_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': None,
            'force_email': True,
            'default_email_from': self.env.user.partner_id.email,
            'default_partner_id_bool': True,
            'default_comp_leave_bool': False,
            'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        }

        if ctx:
            context.update(ctx)

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
    def req_approve(self):
        self.state = "approved"
        self.issued_date = fields.Date.today()
        template_values = {
            'name': 'Confirmation Regarding Compensatory Benefit',
            'subject': 'Confirmation Regarding Compensatory Benefit',
            'body_html': """
                                                               <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                                                   <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                                       <strong>Confirmation Regarding Compensatory Benefit</strong>
                                                                   </p>
                                                                   <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                                       <b>Dear %s,</b>
                                                                   </p>
                                                                   <br/>
                                                                   <br/>
                                                                   <p>
                                                                       Your Compenastory Benefit request has been approved
                                                                   </p>
                                                                   <br/>
                                                                   <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                                       Thank You
                                                                   </p>
                                                               </div>
                                                           """ % (
                self.employee_id.name),
            'model_id': self.env.ref('hr.model_hr_employee').id,
            # Replace 'hr' and 'model_hr_employee' with your actual module and model names
        }
        email_template = self.env['mail.template'].create(template_values)
        mail_template = self.env['mail.template'].browse(email_template.id)

        # Render the email content
        rendered_message = mail_template.body_html

        mail = self.env['mail.mail'].sudo().create({
            'subject': mail_template.subject,
            'body_html': rendered_message,
            'email_from': self.env.user.email,  # Use the actual sender email
            'email_to': self.employee_id.work_email,
        })
        mail.send()

    def req_cancel(self):
        self.state = 'cancel'
        template_values = {
            'name': 'Rejection mail Regarding Compensatory Benefit',
            'subject': 'Rejection mail Regarding Compensatory Benefit',
            'body_html': """
                                                                       <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                                                           <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                                               <strong>Rejection mail Regarding Compensatory Benefit</strong>
                                                                           </p>
                                                                           <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                                               <b>Dear %s,</b>
                                                                           </p>
                                                                           <br/>
                                                                           <br/>
                                                                           <p>
                                                                               Your Compenastory Benefit request has been rejected
                                                                           </p>
                                                                           <br/>
                                                                           <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                                               Thank You
                                                                           </p>
                                                                       </div>
                                                                   """ % (
                self.employee_id.name),
            'model_id': self.env.ref('hr.model_hr_employee').id,
            # Replace 'hr' and 'model_hr_employee' with your actual module and model names
        }
        email_template = self.env['mail.template'].create(template_values)
        mail_template = self.env['mail.template'].browse(email_template.id)

        # Render the email content
        rendered_message = mail_template.body_html

        mail = self.env['mail.mail'].sudo().create({
            'subject': mail_template.subject,
            'body_html': rendered_message,
            'email_from': self.env.user.email,  # Use the actual sender email
            'email_to': self.employee_id.work_email,
        })
        mail.send()


class HrEmployeeNew(models.Model):
    _inherit = 'hr.employee'
    
    def smart_compensatory_request(self):
        self.ensure_one()
        # Find all records related to the current record's employee(s) where is_holiday is True
        all_child = self.env['hr.attendance'].with_context(active_test=False).search([
            ('employee_id', '=', self.id),
            ('is_holiday', '=', True)
        ])

        # Prepare the action for displaying the HR attendances
        action = self.env["ir.actions.act_window"]._for_xml_id("infi_compensatory_request.hr_attendance1_action")
        action['domain'] = [('id', 'in', all_child.ids)]

        return action
    def smart_compensatory_benefit_req(self):
        self.ensure_one()
        # Find all records related to the current record's employee(s) where is_holiday is True
        all_child = self.env['hr.attendance'].with_context(active_test=False).search([
            ('employee_id', '=', self.id)
        ])

        # Prepare the action for displaying the HR attendances
        action = self.env["ir.actions.act_window"]._for_xml_id("infi_compensatory_request.compensatory_request_action")
        action['domain'] = [('id', 'in', all_child.ids)]
        action['context'] = {'search_default_employee_id': self.id}

        return action
    
    def shift_team_action(self):

        action = self.env["ir.actions.act_window"]._for_xml_id("infi_compensatory_request.action_my_team_benefits")


        return action

    def action_compensatory_request(self):
        request_record = self.env['compensatory.request'].create({
            'employee_id': self.id,
        })

        view_id = self.env.ref('infi_compensatory_request.compensatory_request_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Compensatory Request Form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'compensatory.request',
            'target': 'current',
            'res_id': request_record.id,
            'context': {
                 'default_employee_id': self.id,
            }
        }
