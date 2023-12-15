# -*- coding: utf-8 -*-
# from odoo import http


# class CrmDocumentBdhVerification(http.Controller):
#     @http.route('/crm_document_bdh_verification/crm_document_bdh_verification', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_document_bdh_verification/crm_document_bdh_verification/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_document_bdh_verification.listing', {
#             'root': '/crm_document_bdh_verification/crm_document_bdh_verification',
#             'objects': http.request.env['crm_document_bdh_verification.crm_document_bdh_verification'].search([]),
#         })

#     @http.route('/crm_document_bdh_verification/crm_document_bdh_verification/objects/<model("crm_document_bdh_verification.crm_document_bdh_verification"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_document_bdh_verification.object', {
#             'object': obj
#         })
