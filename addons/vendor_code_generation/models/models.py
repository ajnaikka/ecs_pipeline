# -*- coding: utf-8 -*-

from odoo import models, fields, api
from lxml import etree
import json
class ResPartner(models.Model):
    _inherit = 'res.partner'

    unique_reference_id = fields.Char(string='Vendor Code', help="The Unique Sequence no", default='/', store=True)

    @api.model
    def create(self, values):
        res = super(ResPartner, self).create(values)

        if res.supplier_rank == 1:
            suffix = 10000
            res.unique_reference_id = str(suffix + res.id)

        return res



# class SaleOrder(models.Model):
#     _inherit = "sale.order"
#
#
#
#     @api.onchange('partner_id')
#     def _compute_partner_invoice_id(self):
#         res = super(SaleOrder, self)._compute_partner_invoice_id()
#         self.customer_id = self.partner_id.unique_reference_id
#         return res
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    vendor_id = fields.Char(string="Vendor ID")

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        res = super(PurchaseOrder, self).onchange_partner_id()
        self.vendor_id = self.partner_id.unique_reference_id
        return res











