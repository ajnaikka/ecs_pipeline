# -*- coding: utf-8 -*-
# from odoo import http


# class CrmCron(http.Controller):
#     @http.route('/crm_cron/crm_cron/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_cron/crm_cron/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_cron.listing', {
#             'root': '/crm_cron/crm_cron',
#             'objects': http.request.env['crm_cron.crm_cron'].search([]),
#         })

#     @http.route('/crm_cron/crm_cron/objects/<model("crm_cron.crm_cron"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_cron.object', {
#             'object': obj
#         })
