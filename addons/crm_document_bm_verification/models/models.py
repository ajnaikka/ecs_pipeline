# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AttachmentsDetails(models.Model):
    _inherit = 'lead.documents'

    bm_verify = fields.Boolean(default=False, string="BM Verification")

    def verify_document_by_bm(self):
        for record in self:
            record.bm_verify = True


class CrmLead(models.Model):
    _inherit = "crm.lead"

    bm_verified = fields.Boolean(string="BM Verification", default=False, tracking=True)
    bm_verified_date = fields.Datetime('BM Verified Date', tracking=True)
