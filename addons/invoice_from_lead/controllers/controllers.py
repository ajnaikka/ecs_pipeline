# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceFromLead(http.Controller):
#     @http.route('/invoice_from_lead/invoice_from_lead/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_from_lead/invoice_from_lead/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_from_lead.listing', {
#             'root': '/invoice_from_lead/invoice_from_lead',
#             'objects': http.request.env['invoice_from_lead.invoice_from_lead'].search([]),
#         })

#     @http.route('/invoice_from_lead/invoice_from_lead/objects/<model("invoice_from_lead.invoice_from_lead"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_from_lead.object', {
#             'object': obj
#         })
