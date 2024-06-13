# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerIdSequenceGeneration(http.Controller):
#     @http.route('/customer_id_sequence_generation/customer_id_sequence_generation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_id_sequence_generation/customer_id_sequence_generation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_id_sequence_generation.listing', {
#             'root': '/customer_id_sequence_generation/customer_id_sequence_generation',
#             'objects': http.request.env['customer_id_sequence_generation.customer_id_sequence_generation'].search([]),
#         })

#     @http.route('/customer_id_sequence_generation/customer_id_sequence_generation/objects/<model("customer_id_sequence_generation.customer_id_sequence_generation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_id_sequence_generation.object', {
#             'object': obj
#         })
