# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatCustom(http.Controller):
#     @http.route('/openeducat_custom/openeducat_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_custom/openeducat_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_custom.listing', {
#             'root': '/openeducat_custom/openeducat_custom',
#             'objects': http.request.env['openeducat_custom.openeducat_custom'].search([]),
#         })

#     @http.route('/openeducat_custom/openeducat_custom/objects/<model("openeducat_custom.openeducat_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_custom.object', {
#             'object': obj
#         })
