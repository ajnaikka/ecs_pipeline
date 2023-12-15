# -*- coding: utf-8 -*-
# from odoo import http


# class AsbmCorporate(http.Controller):
#     @http.route('/asbm_corporate/asbm_corporate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asbm_corporate/asbm_corporate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('asbm_corporate.listing', {
#             'root': '/asbm_corporate/asbm_corporate',
#             'objects': http.request.env['asbm_corporate.asbm_corporate'].search([]),
#         })

#     @http.route('/asbm_corporate/asbm_corporate/objects/<model("asbm_corporate.asbm_corporate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asbm_corporate.object', {
#             'object': obj
#         })
