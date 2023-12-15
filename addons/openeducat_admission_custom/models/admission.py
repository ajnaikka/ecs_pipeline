# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class OpAdmission(models.Model):
    _inherit = "op.admission"

    payment_type = fields.Selection([('paid', 'Full payment is needed'), ('partial', 'Partial payment is needed')], string="payment Type")

    def admission_confirm(self):
        if not self.payment_type:
            raise UserError(_("Please choose payment type"))
        fee_details = self.env['op.student.fees.details'].search([('op_admission_id', '=', self.id)])
        if any(fee_details.filtered(lambda l: not l.invoice_id)):
            raise ValidationError(_("Please create invoice against all fee details"))
        if self.payment_type == 'paid':
            if any(fee_details.filtered(lambda l: l.invoice_id.payment_state not in ['in_payment', 'paid'])):
                raise ValidationError(_("Make sure all invoice are fully paid"))
            else:
                self.state = 'admission'
        if self.payment_type == 'partial':
            if any(fee_details.filtered(lambda l: l.invoice_id.payment_state not in ['in_payment', 'paid', 'partial'])):
                self.state = 'admission'
            else:
                raise ValidationError(_("Make sure at least one invoice is fully paid or partially paid"))
