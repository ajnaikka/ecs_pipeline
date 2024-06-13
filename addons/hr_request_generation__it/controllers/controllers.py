# -*- coding: utf-8 -*-
# from odoo import http


# class HrRequestGenerationIt(http.Controller):
#     @http.route('/hr_request_generation__it/hr_request_generation__it', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_request_generation__it/hr_request_generation__it/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_request_generation__it.listing', {
#             'root': '/hr_request_generation__it/hr_request_generation__it',
#             'objects': http.request.env['hr_request_generation__it.hr_request_generation__it'].search([]),
#         })

#     @http.route('/hr_request_generation__it/hr_request_generation__it/objects/<model("hr_request_generation__it.hr_request_generation__it"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_request_generation__it.object', {
#             'object': obj
#         })

