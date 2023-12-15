# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class CrmBmDocumentVerification(models.TransientModel):
    _name = 'crm.bm.document.verification'
    _description = 'BM - CRM Document Verification'

    lead_id = fields.Many2one('crm.lead', string="Associated Lead", required=True)
    status = fields.Selection([('verified', 'Verified'), ('missing', 'Missing Documents')], string="Status", required=True)
    verified_date = fields.Datetime('Verified Date', required=True, default=lambda self: fields.Datetime.now())
    message = fields.Html(string="Message", help="Please list out missing documents")

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_lead_id
        to ease window action definitions, and be backward compatible. """
        result = super(CrmBmDocumentVerification, self).default_get(fields_vals)

        if not result.get('lead_id') and self.env.context.get('active_id'):
            result['lead_id'] = self.env.context.get('active_id')
        return result

    def action_verify_documents(self):
        if any(self.lead_id.attachments_details_line.filtered(lambda l: l.bm_verify is False)):
            raise UserError(_("Please verify all documents"))
        if self.status == 'verified':
            self.lead_id.update(
                {
                    'bm_verified': True,
                    'bm_verified_date': self.verified_date,
                }
            )
        else:
            template = self.env.ref('crm_document_bm_verification.missing_documents_bm_email_template', False)
            template.sudo().send_mail(self.id, force_send=True)
