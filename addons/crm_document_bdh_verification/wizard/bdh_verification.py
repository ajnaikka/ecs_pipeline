# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CrmBdhDocumentVerification(models.TransientModel):
    _name = 'crm.bdh.document.verification'
    _description = 'BDH - CRM Document Verification'

    lead_id = fields.Many2one('crm.lead', string="Associated Lead", required=True)
    status = fields.Selection([('verified', 'Verified'), ('missing', 'Missing Documents'), ('declined', 'Declined')], string="Status", required=True)
    delete_declined = fields.Boolean(string="Delete Declined?", default=False)
    verified_date = fields.Datetime('Verified Date', required=True, default=lambda self: fields.Datetime.now())
    message = fields.Html(string="Message", help="Please list out missing documents")
    payment_type = fields.Selection([('paid', 'Full payment is needed'), ('partial', 'Partial payment is needed')],
                                    string="payment Type", required=True)

    @api.model
    def default_get(self, fields_vals):
        """ Allow support of active_id / active_model instead of jut default_lead_id
        to ease window action definitions, and be backward compatible. """
        result = super(CrmBdhDocumentVerification, self).default_get(fields_vals)

        if not result.get('lead_id') and self.env.context.get('active_id'):
            result['lead_id'] = self.env.context.get('active_id')
        return result

    def action_verify_documents(self):
        if any(self.lead_id.attachments_details_line.filtered(lambda l: l.bdh_verification_status is False)):
            raise UserError(_("Please verify all documents"))
        fee_details = self.env['op.student.fees.details'].search([('op_admission_id', '=', self.lead_id.op_admission_id.id)])
        if not fee_details:
            raise ValidationError(_("Please create fee details against admission"))
        if any(fee_details.filtered(lambda l: not l.invoice_id)):
            raise ValidationError(_("Please create invoice against all fee details"))
        if self.payment_type == 'paid':
            if any(fee_details.filtered(lambda l: l.invoice_id.payment_state not in ['in_payment', 'paid'])):
                raise ValidationError(_("Make sure all invoice are fully paid"))
            else:
                self.lead_id.op_admission_id.payment_type = 'paid'
        if self.payment_type == 'partial':
            if any(fee_details.filtered(lambda l: l.invoice_id.payment_state not in ['in_payment', 'paid', 'partial'])):
                self.lead_id.op_admission_id.payment_type = 'partial'
            else:
                raise ValidationError(_("Make sure at least one invoice is fully paid or partially paid"))
        if self.status == 'verified':
            if self.delete_declined is True:
                declined_documents = self.lead_id.attachments_details_line.filtered(lambda l: l.bdh_verification_status == 'declined')
                declined_documents.unlink()
            self.lead_id.update(
                {
                    'bdh_verified': True,
                    'bdh_verified_date': self.verified_date,
                }
            )
        else:
            template = self.env.ref('crm_document_bdh_verification.missing_documents_bdh_email_template', False)
            template.sudo().send_mail(self.id, force_send=True)
