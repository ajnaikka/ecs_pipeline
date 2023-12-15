# -*- coding: utf-8 -*-
# from odoo import http


# class ExamScheduling(http.Controller):
#     @http.route('/exam_scheduling/exam_scheduling', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exam_scheduling/exam_scheduling/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exam_scheduling.listing', {
#             'root': '/exam_scheduling/exam_scheduling',
#             'objects': http.request.env['exam_scheduling.exam_scheduling'].search([]),
#         })

#     @http.route('/exam_scheduling/exam_scheduling/objects/<model("exam_scheduling.exam_scheduling"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exam_scheduling.object', {
#             'object': obj
#         })
