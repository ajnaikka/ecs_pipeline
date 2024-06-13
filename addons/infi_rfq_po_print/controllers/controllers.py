# -*- coding: utf-8 -*-
# from odoo import http


# class InfiRfqPoPrint(http.Controller):
#     @http.route('/infi_rfq_po_print/infi_rfq_po_print', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/infi_rfq_po_print/infi_rfq_po_print/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('infi_rfq_po_print.listing', {
#             'root': '/infi_rfq_po_print/infi_rfq_po_print',
#             'objects': http.request.env['infi_rfq_po_print.infi_rfq_po_print'].search([]),
#         })

#     @http.route('/infi_rfq_po_print/infi_rfq_po_print/objects/<model("infi_rfq_po_print.infi_rfq_po_print"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('infi_rfq_po_print.object', {
#             'object': obj
#         })

