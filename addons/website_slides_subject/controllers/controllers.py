# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteSlidesSubject(http.Controller):
#     @http.route('/website_slides_subject/website_slides_subject', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_slides_subject/website_slides_subject/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_slides_subject.listing', {
#             'root': '/website_slides_subject/website_slides_subject',
#             'objects': http.request.env['website_slides_subject.website_slides_subject'].search([]),
#         })

#     @http.route('/website_slides_subject/website_slides_subject/objects/<model("website_slides_subject.website_slides_subject"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_slides_subject.object', {
#             'object': obj
#         })
