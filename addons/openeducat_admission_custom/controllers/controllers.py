# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatAdmissionCustom(http.Controller):
#     @http.route('/openeducat_admission_custom/openeducat_admission_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_admission_custom/openeducat_admission_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_admission_custom.listing', {
#             'root': '/openeducat_admission_custom/openeducat_admission_custom',
#             'objects': http.request.env['openeducat_admission_custom.openeducat_admission_custom'].search([]),
#         })

#     @http.route('/openeducat_admission_custom/openeducat_admission_custom/objects/<model("openeducat_admission_custom.openeducat_admission_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_admission_custom.object', {
#             'object': obj
#         })
