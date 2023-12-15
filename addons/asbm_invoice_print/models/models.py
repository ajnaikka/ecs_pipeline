# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerBank(models.Model):

    _inherit = 'res.partner.bank'

    bring_in_invoice_print = fields.Boolean(store='True', string="Bring in Invoice Print")


class ResBank(models.Model):
    _inherit = 'res.bank'

    bank_ifsc = fields.Char(store='True', string="IFSC")


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_Bank(self):
        value1 = self.company_id if self.company_id else self.env.company
        bank_id = self.env['res.partner.bank'].search(
            [('company_id', '=', value1.id), ('bring_in_invoice_print', '=', 'true'),
             ('partner_id', '=', value1.partner_id.id)], limit=1)
        return bank_id

