from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockReport(models.Model):
    _inherit = 'product.template'

    stock_out = fields.Float(string='Inventory Out',compute="_compute_stock_out")
    total_quantity = fields.Float(string='Total Quantity',compute="_compute_tot_qty")
    is_camera_unit = fields.Boolean(string='Camera Unit')

    @api.depends('company_id.picking_type','company_id.picking_type.default_location_dest_id')
    def _compute_stock_out(self):
        for line in self:
            source_location = line.env.company.picking_type.default_location_dest_id
            if source_location:
                products_in_location = line.env['stock.quant'].search([
                    ('product_id', '=', line.id),
                    ('location_id', '=', source_location.id)  # Assuming location_id is a Many2one field
                ])
                # Summing up the quantities of products in the location
                total_quantity = sum(products_in_location.mapped('quantity'))
                line.stock_out = total_quantity
            else:
                line.stock_out = 0.0  # or any

    @api.depends('stock_out','qty_available')
    def _compute_tot_qty(self):
        for quantity in self:
            quantity.total_quantity = quantity.stock_out + quantity.qty_available