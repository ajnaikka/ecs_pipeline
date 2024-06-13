from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from markupsafe import Markup


class ConfirmationDescription(models.Model):
    _name = 'confirmation.description'
    _description = 'Confirmation Description'
    _rec_name='employee_id'

    description = fields.Text(string='Description')
    attachment_ids = fields.Many2many('ir.attachment')
    employee_id = fields.Many2one('hr.employee', string="Employee",readonly=True)
    status_bool = fields.Boolean(string="Status",default=False)


    def action_terminate(self):
        return self.action_confirm()

    def action_confirm(self):
        for confirmation in self:
            employee = confirmation.employee_id
            parent_partner_id = employee.hr_manager_id.user_id.partner_id.id
            attachment_ids = [attachment.id for attachment in confirmation.attachment_ids]


            description = confirmation.description or ''


            mail_vals = {
                'subject': f'Probation Confirmation of {employee.name}' if confirmation.status_bool else f'Probation Termination of {employee.name}',
                'body_html': f'<p>Probation of {employee.name} has been confirmed.</p> Description: {description}'
                if confirmation.status_bool else f'<p>Probation of {employee.name} has been Terminated.</p>'
                                                 f' Description: {description}',
                'recipient_ids': [(4, parent_partner_id)],
                'auto_delete': True,
                'attachment_ids': attachment_ids,
            }

            mail_id = self.env['mail.mail'].sudo().create(mail_vals)
            mail_id.send()

            users = self.env['res.users'].search([('partner_id', '=', parent_partner_id)])
            notification_ids = [(0, 0, {
                'res_partner_id': user.partner_id.id,
                'notification_type': 'inbox'
            }) for user in users]

            self.env['mail.message'].create({
                'body': f'<p>Probation of {employee.name} has been confirmed.</p>Description: {description}'


                if confirmation.status_bool else f'<p>Probation of {employee.name} has been Terminated.</p>'
                                                 f' Description: {description}',
                'subject': f'Probation Confirmation  of {employee.name}' if confirmation.status_bool else f'Probation Termination  of {employee.name}',
                'message_type': 'notification',
                'author_id': self.env.user.partner_id.id,
                'notification_ids': notification_ids,
                'partner_ids': [(4, user.partner_id.id) for user in users],
                'attachment_ids': [(6, 0, attachment_ids)]
            })

            message_body = (
                f'<p>Probation of {employee.name} has been confirmed.</p> Description: {description}'
                if confirmation.status_bool else
                f'<p>Probation of {employee.name} has been Terminated. </p>Description: {description}'
            )

            employee.hr_manager_id.message_post(
                body=Markup(message_body),
                subject=(f'Probation Confirmation of {employee.name}' if confirmation.status_bool
                         else f'Probation Termination of {employee.name}'),
                message_type='comment',
                attachment_ids=attachment_ids
            )

        return {
            'type': 'ir.actions.act_url',
            'url': '/web#id=%s&view_type=form&model=hr.employee' % employee.hr_manager_id.id,
            'target': 'self',
        }



class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    probation_start_date = fields.Date(string='Probation Start Date', tracking=True)
    probation_end_date = fields.Date(string='Probation End Date', tracking=True)
    enable_emp_profile_edit = fields.Boolean(string='Enable Edit Profile')


    father_first_name = fields.Char(string='Father Name')
    father_middle_name = fields.Char(string='Father Middle Name')
    father_last_name = fields.Char(string='Father Last Name')
    father_birthday = fields.Date(string='Father Birthday')
    father_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    father_attachment_ids = fields.Many2many('ir.attachment', string="Attachments", relation='father_attachment_rel')

    mother_first_name = fields.Char(string='Mother Name')
    mother_middle_name = fields.Char(string='Mother Middle Name')
    mother_last_name = fields.Char(string='Mother Last Name')
    mother_birthday = fields.Date(string='Mother Birthday')
    mother_gender = fields.Selection([
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other')
    ], string='Gender')
    mother_attachment_ids = fields.Many2many('ir.attachment', string="Attachments", relation='mother_attachment_rel', )

    spouse_first_name = fields.Char(string='Spouse First Name')
    spouse_middle_name = fields.Char(string='Spouse Middle Name')
    spouse_last_name = fields.Char(string='Spouse Last Name')
    spouse_birthday = fields.Date(string='Spouse Birthday')
    spouse_gender = fields.Selection([
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other')
    ], string='Gender')

    spouse_attachment_ids = fields.Many2many('ir.attachment', relation='spouse_attachment_rel', string='Attachment')

    probation_notification_sent = fields.Boolean(string='Probation Notification Sent', copy=False)

    current_contract_start = fields.Date(string="Contract Start Date", related="contract_id.date_start", store=True)

    # father_name = fields.Char(string="Father's Name")
    user_group_bool = fields.Boolean(
        string='User Group Boolean',
        compute='_compute_user_group_bool'
    )

    def _cron_check_probation_validity(self):
        today = fields.Date.today()
        end_date = today + relativedelta(days=15)
        employees = self.search([('probation_end_date', '=', end_date)])

        for employee in employees:

            confirm_button_url = f'/confirm_action/{employee.id}'
            terminate_button_url = f'/terminate_action/{employee.id}'
            confirm_button_text = "Confirm"
            terminate_button_text = "Terminate"

            partner_ids = []
            for email in [employee.parent_id.work_email]:

                partner = self.env['res.partner'].search([('email', '=', email)], limit=1)

                if partner:
                    partner_ids.append(partner.id)

            users = self.env['res.users'].browse(employee.parent_id.user_id.id)

            if users:
                display_msg = (f"Dear {employee.parent_id.name},<br/><br/>The probation extension of {employee.name} "
                               f"is ending within 15 days. Please provide an update from your Odoo portal."
                               f"<br/><br/>Thank you,<br/><br/>{employee.hr_manager_id.name}")

                if employee.probation_notification_sent:
                    display_msg += '<br><br>'

                    display_msg += " Click the button below to submit the report."
                    display_msg += '<br><br>'
                    display_msg += '<div style="display: flex;">'
                    display_msg += ('<a href="{}" style="display: inline-block; '
                                    'background-color: #007bff; color: white; padding: 10px 20px; '
                                    'text-decoration: none; border-radius: 5px; cursor: pointer; margin-left: 10px;">'
                                    '{} </a>'.format(confirm_button_url, confirm_button_text))
                    display_msg += ('<a href="{}" style="display: inline-block; margin-left:10px;'
                                    'background-color: red; color: white; padding: 10px 20px; '
                                    'text-decoration: none; border-radius: 5px; cursor: pointer;">'
                                    '{} </a>'.format(terminate_button_url, terminate_button_text))
                    display_msg += '</div>'

                    display_msg = Markup(display_msg)

                post = employee.parent_id.user_id.partner_id.message_post(subject="Probation Ending Notification",
                                                                          body=display_msg,
                                                                          message_type='notification',
                                                                          subtype_xmlid='mail.mt_comment',
                                                                          author_id=employee.hr_manager_id.user_id.partner_id.id)

                employee.parent_id.message_post(subject="Probation Ending Notification",
                                                body=display_msg,
                                                subtype_xmlid='mail.mt_comment')

                if post:
                    notification_ids = [(0, 0, {'res_partner_id': user.partner_id.id, 'mail_message_id': post.id}) for
                                        user
                                        in users]
                    post.update({'notification_ids': notification_ids})

            body_html = ("The probationary period of %s is ending within 15 days. "
                         ) % (
                            employee.name)

            if employee.probation_notification_sent:
                body_html = (f"Dear {employee.parent_id.name},<br/><br/>The probation extension of {employee.name} "
                             f"is ending within 15 days. Please provide an update from your Odoo portal."
                             f"<br/><br/>Thank you,<br/><br/>{employee.hr_manager_id.name}")

            vals = {
                'subject': 'Probation Ending Notification',
                'body_html': body_html,
                'recipient_ids': [(4, employee.parent_id.user_id.partner_id.id)],
                'auto_delete': True,
            }

            mail_id = self.env['mail.mail'].sudo().create(vals)
            mail_id.send()

            employee.write({'probation_notification_sent': True})

    def action_probation_info(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "inf_employee_certificate_request.action_employee_probation_details")
        action.update({'domain': [('user_ids', 'in', [self.env.user.id])]})
        return action

    def action_certificate_info(self):

        print('sssssssssssssssss',self.aadhar_card)
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "inf_employee_certificate_request.action_employee_certificate")
        return action

    def test(self):
        return self._cron_check_probation_validity()

    def _compute_user_group_bool(self):
        for record in self:
            record.user_group_bool = self.env.user.has_group('hr.group_hr_manager')

    children_ids = fields.One2many('family.member', 'employee_id', string='Children')
    salary_details_ids = fields.One2many('salary.details', 'employee_id', string='Salary Details')

    aadhar_card = fields.Many2many('ir.attachment', relation='aadhar_attachment_rel', string='Aadhar card')
    pan_card = fields.Many2many('ir.attachment', relation='pan_attachment_rel', string='Pan Card')
    tenth_cer = fields.Many2many('ir.attachment', relation='tenth_attachment_rel', string='10th Certificate')
    plus_two_cer = fields.Many2many('ir.attachment', relation='plus_two_attachment_rel', string='Plus Two Certificate')
    graduation = fields.Many2many('ir.attachment', relation='graduation_attachment_rel',
                                  string='Graduation Certificate')
    exp = fields.Many2many('ir.attachment', relation='exp_attachment_rel', string='Experience Certificate')

    # aadhar_card = fields.Binary(string='Aadhar card')
    # pan_card = fields.Binary(string='Pan Card')
    # tenth_cer = fields.Binary(string='10th Certificate')
    # plus_two_cer = fields.Binary(string='Plus Two Certificate')
    # graduation = fields.Binary(string='Graduation Certificate')
    # exp = fields.Binary(string='Experience Certifficate')
    # filename1 = fields.Char(string='Filename 1')
    # filename2 = fields.Char(string='Filename 2')
    # filename3 = fields.Char(string='Filename 3')
    # filename4 = fields.Char(string='Filename 4')
    # filename5 = fields.Char(string='Filename 5')
    # filename6 = fields.Char(string='Filename 5')


class SalaryDetails(models.Model):
    _name = 'salary.details'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    employee_year_id = fields.Many2one('hr.employee', string='Employee')
    type_id = fields.Many2one('hr.salary.rule.category', string="Type")
    amount = fields.Float(string='Monthly Amount')
    amount_year = fields.Float(string='Yearly Amount', compute="_compute_year_amount", store=True)

    @api.depends('amount')
    def _compute_year_amount(self):
        for record in self:
            record.amount_year = record.amount * 12


class FamilyMember(models.Model):
    _name = 'family.member'

    first_name = fields.Char(string='First Name')
    mid_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name')
    birthday = fields.Date(string='Date of birth')
    child_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    children_attachment_ids = fields.Many2many('ir.attachment', string='Attachment')
    relation = fields.Selection([
        ('son', 'Son'),
        ('daughter', 'Daughter'),
    ], string='Relation')
    employee_id = fields.Many2one('hr.employee', string='Employee')
