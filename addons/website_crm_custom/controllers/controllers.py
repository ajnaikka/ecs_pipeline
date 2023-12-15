# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteCrmCustom(http.Controller):
#     @http.route('/website_crm_custom/website_crm_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_crm_custom/website_crm_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_crm_custom.listing', {
#             'root': '/website_crm_custom/website_crm_custom',
#             'objects': http.request.env['website_crm_custom.website_crm_custom'].search([]),
#         })

#     @http.route('/website_crm_custom/website_crm_custom/objects/<model("website_crm_custom.website_crm_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_crm_custom.object', {
#             'object': obj
#         })
