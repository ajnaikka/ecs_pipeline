# -*- coding: utf-8 -*-
# from odoo import http


# class InfiRaiseARequest(http.Controller):
#     @http.route('/infi_raise_a_request/infi_raise_a_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/infi_raise_a_request/infi_raise_a_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('infi_raise_a_request.listing', {
#             'root': '/infi_raise_a_request/infi_raise_a_request',
#             'objects': http.request.env['infi_raise_a_request.infi_raise_a_request'].search([]),
#         })

#     @http.route('/infi_raise_a_request/infi_raise_a_request/objects/<model("infi_raise_a_request.infi_raise_a_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('infi_raise_a_request.object', {
#             'object': obj
#         })

