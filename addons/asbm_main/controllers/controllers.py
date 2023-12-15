# -*- coding: utf-8 -*-
# from odoo import http


# class AsbmMain(http.Controller):
#     @http.route('/asbm_main/asbm_main/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asbm_main/asbm_main/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asbm_main.listing', {
#             'root': '/asbm_main/asbm_main',
#             'objects': http.request.env['asbm_main.asbm_main'].search([]),
#         })

#     @http.route('/asbm_main/asbm_main/objects/<model("asbm_main.asbm_main"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asbm_main.object', {
#             'object': obj
#         })
