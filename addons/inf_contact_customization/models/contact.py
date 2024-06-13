from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_ids = fields.One2many('customer.product', 'partner_id', string='Products')


class CustomerProduct(models.Model):
    _name = 'customer.product'
    _rec_name= 'product_id'

    partner_id = fields.Many2one('res.partner', string='Partner')
    product_id = fields.Many2one('product.product', string='Product')