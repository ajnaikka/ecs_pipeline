# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    hr_manager_id = fields.Many2one('hr.employee', 'HR Manager')

    def smart_raise_request(self):
        self.ensure_one()
        all_child = self.with_context(active_test=False).search([('id', 'in', self.ids)])

        action = self.env["ir.actions.act_window"]._for_xml_id("infi_raise_a_request.raise_request_action")
        action['domain'] = [
            ('employee_id', 'in', all_child.ids)
        ]
        action['context'] = {'search_default_employee_id': self.id}
        return action



    def action_raise_request(self):
        request_record = self.env['raise.request'].create({
            'employee_id': self.id,
        })

        view_id = self.env.ref('infi_raise_a_request.raise_request_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Raise Request Form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'raise.request',
            'target': 'current',
            'res_id': request_record.id,
            'context': {
                'default_employee_id': self.id,
            }
        }





class RaiseRequest(models.Model):
    _name = 'raise.request'
    _description = 'Raise Request'
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
        ('raise_req', 'Raise Request to HR'),
        ('issue_address', 'Issue Addressed'),
        ('to_reporting_manager', 'Assign To Reporting Manager'),
        ('corrected', 'Accepted & Corrected'),
        ('cancel', 'Rejected'),
        ('closed', 'Closed'),
    ], default='draft')


    comment = fields.Text(string="Comment")
    # email_to = fields.Many2one('res.partner', string="To", required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False,
                                 default=lambda self: self.env.company)

    def raise_request_button(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_raise_a_request.employee_raise_request_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'raise.request',
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
        print(context, 'context')

        self.write({'state': 'raise_req'})

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


    def action_issue_address(self):
        for record in self:
            if record.state == 'raise_req':
                record.write({'state': 'issue_address'})
        return True

    def action_assign_reporting_manager(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_raise_a_request.employee_assign_reporting_manager_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'raise.request',
            'default_res_ids': [self.id],
            # 'default_partner_ids': [self.email_to.id],
            'default_raise_req_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': None,
            'force_email': True,
            'default_email_from': self.employee_id.hr_manager_id.work_email,
            'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        }

        if ctx:
            context.update(ctx)
        print(context, 'context')

        self.write({'state': 'to_reporting_manager'})

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

    def action_assign_reporting_manager(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_raise_a_request.employee_assign_reporting_manager_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'raise.request',
            'default_res_ids': [self.id],
            # 'default_partner_ids': [self.email_to.id],
            'default_raise_req_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': None,
            'force_email': True,
            'default_email_from': self.employee_id.hr_manager_id.work_email,
            'default_partner_id': self.employee_id.parent_id.user_partner_id.id
        }

        if ctx:
            context.update(ctx)
        print(context, 'context')

        self.write({'state': 'to_reporting_manager'})

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

    def action_accepted_corrected(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_raise_a_request.employee_accepted_corrected_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'raise.request',
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

    def action_rejected(self, ctx=None):
        self.request_date = fields.Date.today()
        template = self.env.ref('infi_raise_a_request.employee_rejected_email')
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        context = {
            'default_model': 'raise.request',
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

    def close_button(self):
        for record in self:
            if record.state == 'corrected':
                record.write({'state': 'closed'})
        return True