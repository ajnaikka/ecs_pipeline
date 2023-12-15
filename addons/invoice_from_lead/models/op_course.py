from odoo import models, fields, api


class opCourse(models.Model):
    _inherit = "op.course"

    is_product=fields.Boolean("Is Product")
    list_price = fields.Float('Product Price')
    product_id = fields.Many2one('product.product', string="Product")

    def write(self, vals):
        result = super(opCourse, self).write(vals)

        return result
        # if result.is_product:
        #     product_data = {
        #         'name': result.name,
        #         'list_price': result.list_price,
        #     }
        #     product_result = self.env['product.product'].write(product_data)



    @api.model
    def create(self,vals_list):
        result = super(opCourse, self).create(vals_list)
        if vals_list['is_product'] == True:
            product_data = {
                'name': result.name,
                'list_price': result.list_price,
                'type': 'service',
                'uom_id': 1,
                'uom_po_id': 1,
                'categ_id': 1,
            }
            product_result = self.env['product.product'].create(product_data)
            result.product_id = product_result.id
        return result













