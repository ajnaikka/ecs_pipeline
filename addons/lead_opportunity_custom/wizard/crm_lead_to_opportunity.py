# -*- coding: utf-8 -*-
from datetime import date, datetime, time
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    partner_id = fields.Many2one(domain="[('is_student', '=', True)]", string="Student")
    user_id = fields.Many2one(string="Counsellor")

    def action_apply(self):
        leads = self.env['crm.lead'].browse(self._context.get('active_ids', []))
        if self.action == 'create' and any(leads.filtered(lambda l: not l.contact_name or not l.email_from or not l.portal_email_state or l.portal_email_state != 'ok')):
            raise UserError(_('Please provide contact name and valid email'))
        if self.action == 'exist' and any(leads.filtered(lambda l: not l.contact_name or not l.email_from)):
            raise UserError(_('Please provide contact name and valid email'))
        res = super().action_apply()
        for lead in leads:
            lead.with_context(default_user_id=self.user_id.id)._handle_partner_portal_user_assignment()
        return res
