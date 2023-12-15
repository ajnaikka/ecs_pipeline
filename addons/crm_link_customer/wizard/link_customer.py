# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class CrmLinkCustomer(models.TransientModel):
    _name = 'crm.link.customer'
    _description = 'CRM Link Customer'

    lead_id = fields.Many2one('crm.lead', string="Associated Lead", required=True)
    action = fields.Selection([
        ('create', 'Create a new customer'),
        ('exist', 'Link to an existing customer')
    ], string='Related Customer', compute='_compute_action', readonly=False, store=True, compute_sudo=False)
    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        compute='_compute_partner_id', readonly=False, store=True, compute_sudo=False)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True)

    @api.depends('lead_id')
    def _compute_action(self):
        for convert in self:
            if not convert.lead_id:
                convert.action = 'create'
            else:
                partner = convert.lead_id._find_matching_partner()
                if partner:
                    convert.action = 'exist'
                elif convert.lead_id.contact_name:
                    convert.action = 'create'
                else:
                    convert.action = 'create'

    @api.depends('action', 'lead_id')
    def _compute_partner_id(self):
        for convert in self:
            if convert.action == 'exist':
                convert.partner_id = convert.lead_id._find_matching_partner()
            else:
                convert.partner_id = False

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_lead_id
        to ease window action definitions, and be backward compatible. """
        result = super(CrmLinkCustomer, self).default_get(fields_vals)

        if not result.get('lead_id') and self.env.context.get('active_id'):
            result['lead_id'] = self.env.context.get('active_id')
        if result.get('lead_id'):
            lead = self.env['crm.lead'].browse(result['lead_id'])
            result['user_id'] = lead.user_id.id or self.env.user.id
        return result

    def action_apply(self):
        leads = self.env['crm.lead'].browse(self._context.get('active_ids', []))
        if self.action == 'create' and any(leads.filtered(lambda l: not l.contact_name or not l.email_from or not l.portal_email_state or l.portal_email_state != 'ok')):
            raise UserError(_('Please provide contact name and valid email'))
        if self.action == 'exist' and any(leads.filtered(lambda l: not l.contact_name or not l.email_from)):
            raise UserError(_('Please provide contact name and valid email'))
        for lead in leads:
            lead.with_context(default_user_id=self.user_id.id)._handle_partner_assignment(
                force_partner_id=self.partner_id.id or lead.partner_id.id, create_missing=(self.action == 'create')
            )
            lead.with_context(default_user_id=self.user_id.id)._handle_partner_portal_user_assignment()
