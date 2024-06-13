from odoo import models, fields, api, exceptions, _
from datetime import timedelta


class ShiftMaster(models.Model):
    _name = 'shift.master'
    _description = 'Shift Master'
    _rec_name = 'name'

    name = fields.Char(string='shift')
    start_time = fields.Float(string='Start Time')
    end_time = fields.Float(string='End Time')
    shift_type = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('general', 'General'),
    ], string='Shift Type')


class ShiftRequest(models.Model):
    _name = 'shift.request'
    _description = 'Shift Request'
    _rec_name = 'name'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    shift_id = fields.Many2one('shift.master', string='Shift')
    shift_from = fields.Date(string='Start Date')
    shift_to = fields.Date(string='End Date')
    color = fields.Char(string='Color')
    project_manager_id = fields.Many2one('hr.employee', string="Project Manager", related='employee_id.parent_id',
                                         store=True)
    start_time = fields.Float(string='Start Time', readonly=True, related="shift_id.start_time")
    end_time = fields.Float(string='End Time', readonly=True, related="shift_id.end_time")

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    shifts_count_in_week = fields.Integer(string='Shifts Count in Week', compute='_compute_shifts_count')

    state = fields.Selection([
        ('confirm', 'Confirm'),

        ('request', 'Request'),
        ('reject', 'Reject'),
    ], string='State', default='confirm')

    def action_reject(self):
        self.state = 'reject'

    def action_confirm(self):
        self.state = 'confirm'

    current_user_name = fields.Char(string='Current User Name', compute='_compute_current_user_name')

    # Compute function to get the name of the current user

    def _compute_current_user_name(self):
        for record in self:
            if record.employee_id and record.employee_id.user_id:
                record.current_user_name = record.employee_id.user_id.name
            else:
                record.current_user_name = ''

    @api.model
    def _fetching_current_user(self):
        employee_id = self.env.user.employee_id.id
        print("employee_id", employee_id)
        return employee_id

    @api.model
    def get_current_user_employee_id_domain(self):
        employee_id = self.env.user.employee_id.id
        domain = [('employee_id', '=', employee_id)]
        return domain

    @api.depends('shifts_count_in_week', 'shift_id')
    def _compute_name(self):
        for record in self:
            # Check if both employee_id and shift_id are set
            if record.employee_id and record.shift_id:
                # Check the shifts_count_in_week to determine the suffix for the name
                if record.shifts_count_in_week > 5:
                    record.name = '%s - %s' % (record.shift_id.name, 'Comb Off')
                else:
                    record.name = '%s' % (record.shift_id.name)
            else:
                # If either employee_id or shift_id is not set, use 'Undefined'
                record.name = 'Undefined'

    @api.depends('employee_id', 'shift_from')
    def _compute_shifts_count(self):
        for record in self:
            if record.employee_id and record.shift_from:
                # Calculate the start and end dates of the week
                start_of_week = record.shift_from - timedelta(days=record.shift_from.weekday())
                end_of_week = start_of_week + timedelta(days=6)

                # Count the number of shifts for the employee within the week
                shifts_count = self.env['shift.request'].search_count([
                    ('employee_id', '=', record.employee_id.id),
                    ('shift_from', '>=', start_of_week),
                    ('shift_from', '<=', end_of_week)
                ])
                record.shifts_count_in_week = shifts_count
            else:
                record.shifts_count_in_week = 0

    @api.model
    def create(self, vals):
        # First, call super to create the record
        record = super(ShiftRequest, self).create(vals)

        # Now, prepare and send the email
        record.send_shift_request()
        record.send_shift_compensatory()

        return record

    def send_shift_request(self):
        if self.shifts_count_in_week > 5:
            template_values = {
                'name': 'Mail Regarding Shift',
                'subject': 'Mail Regarding Shift',
                'body_html': """
                                           <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                               <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                   <strong>Mail Regarding Shift</strong>
                                               </p>
                                               <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                   <b>Dear %s,</b>
                                               </p>
                                               <br/>
                                               <br/>
                                               <p>
                                                   Your are allocated %s shift on %s and are eligible for compensatory benefit
                                               </p>
                                               <br/>
                                               <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                   Thank You
                                               </p>
                                           </div>
                                                                                   """ % (
                    self.employee_id.name, self.shift_id.name, self.shift_from),
                'model_id': self.env.ref('infi_compensatory_request.model_shift_request').id,
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

        else:
            body = """
                <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                    <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                        <strong>Mail Regarding Shift</strong>
                    </p>
                    <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                        <b>Dear %s,</b>
                    </p>
                    <br/>
                    <br/>
                    <p>
                        You are allocated %s shift%s
                    </p>
                    <br/>
                    <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                        Thank You
                    </p>
                </div>
            """ % (self.employee_id.name, self.shift_id.name,
                   f" from {self.shift_from} to {self.shift_to}" if self.shift_from and self.shift_to else f" on {self.shift_from}")

            template_values = {
                'name': 'Mail Regarding Shift',
                'subject': 'Mail Regarding Shift',
                'body_html': body,
                'model_id': self.env.ref('infi_compensatory_request.model_shift_request').id,
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
            print(mail, 'mail')
            mail.send()

    def send_shift_compensatory(self):
        pass
        # if self.shifts_count_in_week > 5:
        #     template_values = {
        #         'name': 'Mail Regarding compensatory benefit',
        #         'subject': 'Mail Regarding Shift',
        #         'body_html': """
        #                                    <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
        #                                        <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
        #                                            <strong>Mail Regarding Shift</strong>
        #                                        </p>
        #                                        <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
        #                                            <b>Dear %s,</b>
        #                                        </p>
        #                                        <br/>
        #                                        <br/>
        #                                        <p>
        #                                            Your are eligible for compensatory benefit
        #                                        </p>
        #                                        <br/>
        #                                        <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
        #                                            Thank You
        #                                        </p>
        #                                    </div>
        #                                                                        """ % (
        #             self.employee_id.name),
        #         'model_id': self.env.ref('infi_compensatory_request.model_shift_request').id,
        #         # Replace 'hr' and 'model_hr_employee' with your actual module and model names
        #     }
        #     email_template = self.env['mail.template'].create(template_values)
        #     mail_template = self.env['mail.template'].browse(email_template.id)
        #
        #     # Render the email content
        #     rendered_message = mail_template.body_html
        #
        #     mail = self.env['mail.mail'].sudo().create({
        #         'subject': mail_template.subject,
        #         'body_html': rendered_message,
        #         'email_from': self.env.user.email,  # Use the actual sender email
        #         'email_to': self.employee_id.work_email,
        #     })
        #     print(mail, 'mail')
        #     mail.send()
        #
        # else:
