# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class LeadDocumentsBdhVerification(models.TransientModel):
    _name = 'lead.documents.bdh.verification'
    _description = 'Lead Documents BDH Verification'

    lead_document_id = fields.Many2one('lead.documents', string="Lead Document", required=True)
    status = fields.Selection([('verified', 'Verified'), ('declined', 'Declined')], string="Status", required=True)
    reason = fields.Text(string="Reason")

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_lead_id
        to ease window action definitions, and be backward compatible. """
        result = super(LeadDocumentsBdhVerification, self).default_get(fields_vals)

        if not result.get('lead_document_id') and self.env.context.get('active_id'):
            result['lead_document_id'] = self.env.context.get('active_id')
        return result

    def action_verify_documents(self):
        self.lead_document_id.update(
            {
                'bdh_verification_status': self.status,
                'bdh_decline_reason': self.reason,
            }
        )
