from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BoQComponent(models.Model):
    _name = 'kit.component'
    _inherit = 'mail.thread'
    _description = 'BoQ Component'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', string="Product")
    product_line_ids = fields.One2many(
        'kit.component.line', 'boq_id', string='Required Products', copy=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed')],
        default='draft', readonly=True)
    quantity = fields.Float(string='Quantity',default=1)
    uom_id = fields.Many2one('uom.uom',related="product_id.product_tmpl_id.uom_id",string='Unit')

    def action_validate(self):
        boq = self.env['kit.component'].search([('product_id', '=', self.product_id.id), ('state', '=', 'confirmed')])
        if len(boq) > 1:
            raise ValidationError(
                _(
                    "The Boq of the current product has been already created."
                ))
        self.state = 'confirmed'

    def action_reset(self):
        self.state = 'draft'


class BoQComponentLine(models.Model):
    _name = 'kit.component.line'
    _description = 'BoQ Component Line'

    boq_id = fields.Many2one('kit.component', string='BoQ')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float('Quantity', default=1)
    uom_id = fields.Many2one('uom.uom', string='Unit')
    slno = fields.Integer('No.', compute="_compute_get_number", store=True)

    @api.depends('boq_id.product_line_ids', 'boq_id.product_line_ids.product_id')
    def _compute_get_number(self):
        for line in self:
            no = 0
            line.slno = no
            for l in line.boq_id.product_line_ids:
                no += 1
                l.slno = no

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id