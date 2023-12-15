# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Lead(models.Model):
    _inherit = "crm.lead"

    op_admission_id = fields.Many2one('op.admission', string="Admission")
    op_admission_status = fields.Selection(string='Admission Status', related='op_admission_id.state')
    fees_details_count = fields.Integer(compute='_compute_fees_details')
    batch_id = fields.Many2one('op.batch', string='Batch')
    batch_type = fields.Selection([('normal', 'Normal'), ('emergency', 'Emergency'), ('super', 'Super Emergency')],
                                  string="Batch Type")
    course_extra_fees_line = fields.One2many(
        comodel_name='course.extra.fees',
        inverse_name='lead_id',
        string="Extra Fee Lines",
        copy=True, auto_join=True)
    extra_fees = fields.Float(string='Extra Course Fee', compute='compute_course_fee', store=True)
    total_course_fee = fields.Float(string="Total Course Fee", compute='compute_course_fee', store=True)

    @api.depends('course_extra_fees_line.price', 'course_fees')
    def compute_course_fee(self):
        for record in self:
            record.extra_fees = sum(line.price for line in record.course_extra_fees_line) if record.course_extra_fees_line else 0.0
            record.total_course_fee = record.extra_fees + record.course_fees

    @api.depends('op_admission_id')
    def _compute_fees_details(self):
        for record in self:
            if record.op_admission_id:
                record.fees_details_count = self.env['op.student.fees.details'].search_count(
                    [('op_admission_id', '=', self.op_admission_id.id)])
            else:
                record.fees_details_count = 0

    def view_student_fees_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fees Details',
            'view_mode': 'tree',
            'res_model': 'op.student.fees.details',
            'context': {'create': False},
            'domain': [('op_admission_id', '=', self.op_admission_id.id)],
            'target': 'current',
        }

    def action_generate_application(self):
        pass


class CourseExtraFees(models.Model):
    _name = 'course.extra.fees'
    _description = 'Course Extra Fees'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    price = fields.Float(string='Price', required=True, digits='Product Price')
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string="Lead Reference",
        required=True, ondelete='cascade', index=True, copy=False)


class OpStudentFeesDetails(models.Model):
    _inherit = "op.student.fees.details"

    lead_id = fields.Many2one('crm.lead', string="Lead Reference")

    def get_invoice(self):
        if self.lead_id:
            inv_obj = self.env['account.move']
            partner_id = self.student_id.partner_id
            account_id = False
            product = self.product_id
            if product.property_account_income_id:
                account_id = product.property_account_income_id.id
            if not account_id:
                account_id = product.categ_id.property_account_income_categ_id.id
            if not account_id:
                raise UserError(
                    _('There is no income account defined for this product: "%s".'
                      'You may have to install a chart of account from Accounting'
                      ' app, settings menu.') % product.name)
            if self.amount <= 0.00:
                raise UserError(
                    _('The value of the deposit amount must be positive.'))
            else:
                amount = self.amount
                name = product.name
            invoice = inv_obj.create({
                'move_type': 'out_invoice',
                'partner_id': partner_id.id,
                'invoice_date_due': self.date,

            })
            line_values = {'name': name,
                           'account_id': account_id,
                           'price_unit': (self.lead_id.course_fees * self.fees_line_id.value) / 100,
                           'quantity': 1.0,
                           'discount': self.discount or False,
                           'product_uom_id': product.uom_id.id,
                           'product_id': product.id}
            invoice.write({'invoice_line_ids': [(0, 0, line_values)]})
            for record in self.lead_id.course_extra_fees_line:
                if record:
                    line_values = {'name': record.product_id.name,
                                   'account_id': record.product_id.property_account_income_id.id or record.product_id.categ_id.property_account_income_categ_id.id,
                                   'price_unit': (record.price * self.fees_line_id.value) / 100,
                                   'quantity': 1.0,
                                   'discount': self.discount or False,
                                   'product_uom_id': record.product_id.uom_id.id,
                                   'product_id': record.product_id.id, }
                    invoice.write({'invoice_line_ids': [(0, 0, line_values)]})
            invoice._compute_tax_totals()
            self.state = 'invoice'
            self.invoice_id = invoice.id
            return True
