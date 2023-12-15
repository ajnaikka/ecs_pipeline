# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OpStudentFeesDetails(models.Model):
    _inherit = "op.student.fees.details"

    payment_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ], string='Payment Status', copy=False, compute='_compute_payment_state', store=True, readonly=True,)

    @api.depends('invoice_id', 'invoice_id.payment_state')
    def _compute_payment_state(self):
        for record in self:
            record.payment_state = 'draft'
            if record.invoice_id:
                if record.invoice_id.payment_state == 'not_paid':
                    record.payment_state = 'draft'
                elif record.invoice_id.payment_state == 'partial':
                    record.payment_state = 'pending'
                elif record.invoice_id.payment_state in ('in_payment', 'paid'):
                    record.payment_state = 'completed'
                else:
                    record.payment_state = 'completed'
