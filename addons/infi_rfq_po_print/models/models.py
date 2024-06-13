# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from num2words import num2words



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    reference_no_date = fields.Char(string='Reference No & Date')
    vat =  fields.Char(string='GST No',related='partner_id.vat')
    dispatched_through = fields.Char(string='Dispatched through')
    destination = fields.Char(string='Destination')

    def english_amt2words(self, amount, currency, change, precision):
        change_amt = (amount - int(amount)) * pow(10, precision)
        words = '{main_amt} {main_word}'.format(
            main_amt=num2words(int(amount)),
            main_word=currency,
        )
        change_amt = int(round(change_amt))
        # words = words.title()
        if change_amt > 0:
            words += ' and {change_amt} {change_word}'.format(
                change_amt=num2words(change_amt),
                change_word=change,
            )
        words = words.title()
        words = words.replace('And', 'and')
        words = words.replace(',', '')
        words = words + ' Only'
        return words
