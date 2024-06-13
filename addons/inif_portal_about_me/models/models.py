# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class inif_portal_about_me(models.Model):
#     _name = 'inif_portal_about_me.inif_portal_about_me'
#     _description = 'inif_portal_about_me.inif_portal_about_me'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

