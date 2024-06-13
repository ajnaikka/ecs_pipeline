# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    def smart_generate_it_request(self):
        self.ensure_one()
        all_child = self.with_context(active_test=False).search([('id', 'in', self.ids)])

        action = self.env["ir.actions.act_window"]._for_xml_id("hr_request_generation__it.generate_it_request_action")
        action['domain'] = [
            ('employee_id', 'in', all_child.ids)
        ]
        action['context'] = {'search_default_employee_id': self.id}
        return action



    def action_generate_it_request(self):
        request_record = self.env['request.it'].create({
            'employee_id': self.id,
            'job_id': self.job_id.id if self.job_id else False,
        })

        view_id = self.env.ref('hr_request_generation__it.generate_it_request_form').id

        employee_name = self.name

        return {
            'type': 'ir.actions.act_window',
            'name': 'Generate IT Request Form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'request.it',
            'target': 'current',
            'res_id': request_record.id,
            'context': {
                'default_employee_id': self.id,
                'default_job_id': self.job_id,
                'default_employee_name': employee_name,
            }
        }





class RequestIT(models.Model):
    _name = 'request.it'
    _description = 'Request IT '
    _order = 'id desc'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    request_date = fields.Date(string='Request Date', format='%d-%m-%y')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    job_id = fields.Many2one(string="designation",related='employee_id.job_id')
    work_email = fields.Char(related='employee_id.work_email', readonly=False, related_sudo=False)

    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('gen_req', 'Generate Request to IT'),
        ('issue_address_to_it', 'Issue Addressed by IT'),

    ], default='draft')


    comment = fields.Text(string="Comment")
    # email_to = fields.Many2one('res.partner', string="To", required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False,
                                 default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if 'default_employee_id' in self._context:
            employee_id = self._context.get('default_employee_id')
            vals['employee_id'] = employee_id
        # if 'default_job_id' in self._context:
        #     job_id = self._context.get('default_job_id')
        #     vals['job_id'] = job_id
        return super(RequestIT, self).create(vals)

    it_team_emails = fields.Many2many(
        'res.users', string='IT Team',
        compute='_compute_it_team_emails', store=True,
        relation='it_team_emails_relation'
    )


    @api.depends('company_id')
    def _compute_it_team_emails(self):
        it_team_group = self.env.ref('infinous_user_groups.it_department')
        self.it_team_emails = it_team_group.users

    def generate_it_request_button(self, ctx=None):
        self.request_date = fields.Date.today()
        email_body = f"""Dear IT Team,<br/><br/>
               Request to generate work mail id for:
               <br/>
               Employee Name:  {self.employee_id.name}
               <br/>
               Employee Designation:  {self.job_id.name}
               <br/>
               <br/>
               Best regards,<br/>
               HR Department<br/>
               """

        # Send email
        it_team_emails = ', '.join(user.work_email for user in self.it_team_emails)
        mail_values = {
            'subject': f'Work mail generation request for {self.employee_id.name}',
            'body_html': email_body,
            'email_from': self.employee_id.hr_manager_id.work_email,
            'email_to': it_team_emails,
        }
        self.env['mail.mail'].create(mail_values).send()

        self.write({'state': 'gen_req'})

        return True
        # template = self.env.ref('hr_request_generation__it.employee_generate_it_request_email')
        # compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        #
        # context = {
        #     'default_model': 'request.it',
        #     'default_res_ids': [self.id],
        #     # 'default_partner_ids': [self.email_to.id],
        #     'default_raise_req_id': self.id,
        #     'default_use_template': bool(template),
        #     'default_template_id': template.id,
        #     'default_composition_mode': 'comment',
        #     'default_attachment_ids': None,
        #     'force_email': True,
        #     'default_email_from': self.employee_id.hr_manager_id.work_email,
        #     'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        # }
        #
        # if ctx:
        #     context.update(ctx)
        # print(context, 'context')
        #
        # self.write({'state': 'gen_req'})
        #
        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'mail.compose.message',
        #     'views': [(compose_form_id, 'form')],
        #     'views_id': compose_form_id,
        #     'target': 'new',
        #     'context': context,
        # }

    def action_issue_address_by_it(self, ctx=None):
        self.request_date = fields.Date.today()
        email_body = f"""Dear HR Manager,<br/><br/>
        The work email - id of {self.employee_id.name} has been generated. 
        <br/>
        <br/>
       
        <br/>
        Best regards,<br/>
        IT Department<br/>
        """

        # Send email
        mail_values = {
            'subject': 'Work Mail ID generated',
            'body_html': email_body,
            'email_from': self.env.user.work_email,
            'email_to': self.employee_id.hr_manager_id.work_email,
        }
        self.env['mail.mail'].create(mail_values).send()

        self.write({'state': 'issue_address_to_it'})

        return True
        # template = self.env.ref('hr_request_generation__it.employee_issue_address_by_it_email')
        # compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        #
        # context = {
        #     'default_model': 'request.it',
        #     'default_res_ids': [self.id],
        #     # 'default_partner_ids': [self.email_to.id],
        #     'default_raise_req_id': self.id,
        #     'default_use_template': bool(template),
        #     'default_template_id': template.id,
        #     'default_composition_mode': 'comment',
        #     'default_attachment_ids': None,
        #     'force_email': True,
        #     'default_email_from': self.env.user.work_email,
        #     'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        # }
        #
        # if ctx:
        #     context.update(ctx)
        # print(context, 'context')
        #
        # self.write({'state': 'issue_address_to_it'})
        #
        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'mail.compose.message',
        #     'views': [(compose_form_id, 'form')],
        #     'views_id': compose_form_id,
        #     'target': 'new',
        #     'context': context,
        # }
