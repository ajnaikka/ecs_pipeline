from odoo import models, fields, api, _

from odoo.exceptions import UserError


class HrEmployeeHeadcount(models.Model):
    _inherit = 'hr.employee'

    # refuse_approve_checking_for_reporting_manager = fields.Boolean(string="Check Refuse And Approve")


    def recruitment_request(self):
        request_record = self.env['headcount.request'].create({
            'employee_id': self.id,
        })

        view_id = self.env.ref('infi_headcount_request.raise_request_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Head Count Request Form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'headcount.request',
            'target': 'current',
            'res_id': request_record.id,
            'context': {
                'default_employee_id': self.id,
            }
        }


class HeadcountRequest(models.Model):
    _name = 'headcount.request'
    _description = 'Head Count Request'
    _order = 'id desc'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    request_date = fields.Date(string='Request Date', default=fields.Date.today, format='%d-%m-%y', readonly=True)

    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
    )
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('req_to_superior', 'Raise Request to Superior'),
        ('issue_address', 'Issue Addressed To HR'),

    ], default='draft')

    comment = fields.Text(string="Comment")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False,
                                 default=lambda self: self.env.company)

    def action_refusing_dup(self):
        print("===")

        if self.state in ['draft', 'req_to_superior', 'issue_address', 'issue_addressed']:
            return {
                'name': _('Refuse Recruitment Request'),
                'type': 'ir.actions.act_window',
                'views': [(False, 'form')],
                'view_mode': 'form',
                'view_id': self.env.ref('infi_headcount_request.raise_request_view_form').id,
                'res_model': 'headcount.request.wizard',
                'context': {'default_employee_id': self.employee_id.id},

                # 'res_id': wizard.id,
                'target': 'new',
            }

    def head_count_recruitment_request(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_headcount_request.employee_recruitment_request_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'headcount.request',
            'default_res_ids': [self.id],
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
        print(context, 'context')

        self.write({'state': 'req_to_superior'})

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

    def head_count_recruitment_request(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_headcount_request.employee_recruitment_request_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'headcount.request',
            'default_res_ids': [self.id],
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
        print(context, 'context')

        self.write({'state': 'req_to_superior'})

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

    def head_count_recruitment_request_to_hr(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_headcount_request.employee_recruitment_request_email2')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'headcount.request',
            'default_res_ids': [self.id],
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
        print(context, 'context')

        self.write({'state': 'issue_address'})

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

    def head_count_recruitment_request_to_hr_to_superior(self, ctx=None):
        self.action_send_message_to_report_manager()
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_headcount_request.employee_recruitment_request_email1')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'headcount.request',
            'default_res_ids': [self.id],
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

        self.write({'state': 'issue_addressed'})

        print(context, 'context')

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

    def action_send_message_to_report_manager(self):
        template_values = {
            'name': 'Mail Regarding to Refuse Recruitment Request',
            'subject': "self",
            'body_html': """
                                                       <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                                           <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                               <strong>Refuse Recruitment Request</strong>
                                                           </p>
                                                           <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                               <b>Dear %s,</b>
                                                           </p>
                                                           <br/>
                                                           <br/>
                                                           <p>
                                                               Recruitment Request has been cancelled,Please Contact Concerned assignment team for further enquiries
                                                           </p>
                                                           <br/>
                                                           <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                               Thank You
                                                           </p>
                                                       </div>
                                                   """ % (self.employee_id.name),
            'model_id': self.env.ref('infi_headcount_request.model_headcount_request_wizard').id,
        }

        email_templates = self.env['mail.template'].create(template_values)

        mail_template = self.env['mail.template'].browse(email_templates.id)

        rendered_message = mail_template.body_html

        mail = self.env['mail.mail'].sudo().create({
            'subject': mail_template.subject,
            'body_html': rendered_message,
            'email_from': self.env.user.email,  # Use the actual sender email self.env.user.email,
            'email_to': self.user_id.employee_id.work_email,
        })
        print("from mail=", self.env.user.email)
        mail.send()


class RecruitmentRefuseWizard(models.TransientModel):
    _name = 'headcount.request.wizard'

    reason = fields.Char(string="Reason")
    user_id = fields.Many2one('res.user', 'user')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    state = fields.Selection([
        ('refuse', 'Refuse'),
    ])

    def action_send_message(self):
        template_values = {
            'name': 'Mail Regarding to Refuse Recruitment Request',
            'subject': self.reason,
            'body_html': """
                                                       <div style="font-family: Arial, sans-serif; max-width: 1400px; margin: auto; border: 1px solid #fff; direction: ltr;">
                                                           <p style="text-align: center; font-size: 18px; color: #333; margin-bottom: 20px;">
                                                               <strong>Refuse Recruitment Request</strong>
                                                           </p>
                                                           <p style="text-align: left; font-size: 18px; color: #333; margin-bottom: 20px;" >
                                                               <b>Dear %s,</b>
                                                           </p>
                                                           <br/>
                                                           <br/>
                                                           <p>
                                                               Recruitment Request has been cancelled,Please Contact Concerned assignment team for further enquiries
                                                           </p>
                                                           <br/>
                                                           <p style="text-align: left; font-size: 16px; color: #333; margin-top: 20px;">
                                                               Thank You
                                                           </p>
                                                       </div>
                                                   """ % (self.employee_id.name),
            'model_id': self.env.ref('infi_headcount_request.model_headcount_request_wizard').id,
        }

        email_templates = self.env['mail.template'].create(template_values)

        mail_template = self.env['mail.template'].browse(email_templates.id)

        rendered_message = mail_template.body_html

        mail = self.env['mail.mail'].sudo().create({
            'subject': mail_template.subject,
            'body_html': rendered_message,
            'email_from': self.employee_id.parent_id.work_email,
            'email_to': self.employee_id.work_email,
        })

        mail.send()
        return True


