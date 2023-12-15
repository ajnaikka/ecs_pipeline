# -*- coding: utf-8 -*-
# from odoo import http


# class LeadOpportunityCustom(http.Controller):
#     @http.route('/lead_opportunity_custom/lead_opportunity_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lead_opportunity_custom/lead_opportunity_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lead_opportunity_custom.listing', {
#             'root': '/lead_opportunity_custom/lead_opportunity_custom',
#             'objects': http.request.env['lead_opportunity_custom.lead_opportunity_custom'].search([]),
#         })

#     @http.route('/lead_opportunity_custom/lead_opportunity_custom/objects/<model("lead_opportunity_custom.lead_opportunity_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lead_opportunity_custom.object', {
#             'object': obj
#         })
