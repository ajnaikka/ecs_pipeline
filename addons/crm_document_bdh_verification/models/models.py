# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AttachmentsDetails(models.Model):
    _inherit = 'lead.documents'

    bdh_verification_status = fields.Selection([('verified', 'Verified'), ('declined', 'Declined')], string="Backend Verification")
    bdh_decline_reason = fields.Text(string="Verification Decline reason")


class CrmLead(models.Model):
    _inherit = "crm.lead"

    bdh_verified = fields.Boolean(string="Backend Verification", default=False, tracking=True)
    bdh_verified_date = fields.Datetime('Backend Verified Date', tracking=True)
