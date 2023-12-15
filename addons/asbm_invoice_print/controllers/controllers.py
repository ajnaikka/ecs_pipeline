# -*- coding: utf-8 -*-
# from odoo import http


# class AsbmInvoicePrint(http.Controller):
#     @http.route('/asbm_invoice_print/asbm_invoice_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asbm_invoice_print/asbm_invoice_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asbm_invoice_print.listing', {
#             'root': '/asbm_invoice_print/asbm_invoice_print',
#             'objects': http.request.env['asbm_invoice_print.asbm_invoice_print'].search([]),
#         })

#     @http.route('/asbm_invoice_print/asbm_invoice_print/objects/<model("asbm_invoice_print.asbm_invoice_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asbm_invoice_print.object', {
#             'object': obj
#         })
