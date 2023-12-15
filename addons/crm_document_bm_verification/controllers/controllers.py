# -*- coding: utf-8 -*-
# from odoo import http


# class CrmDocumentBmVerification(http.Controller):
#     @http.route('/crm_document_bm_verification/crm_document_bm_verification', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_document_bm_verification/crm_document_bm_verification/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_document_bm_verification.listing', {
#             'root': '/crm_document_bm_verification/crm_document_bm_verification',
#             'objects': http.request.env['crm_document_bm_verification.crm_document_bm_verification'].search([]),
#         })

#     @http.route('/crm_document_bm_verification/crm_document_bm_verification/objects/<model("crm_document_bm_verification.crm_document_bm_verification"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_document_bm_verification.object', {
#             'object': obj
#         })
